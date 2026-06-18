"""
SeLoger scraper — intercepts internal API calls from the map view.

Strategy: Playwright renders the page with a real browser, we intercept
the network requests SeLoger's frontend makes to its own API, and capture
the raw JSON listings — no HTML parsing needed.

Setup (run once):
    pip install playwright pandas
    python -m playwright install chromium

Usage:
    python scraper.py
    → outputs seloger_listings.json and seloger_listings.csv
"""

import asyncio
import json
import re
import pandas as pd
from datetime import datetime
from playwright.async_api import async_playwright

# ── Your search URL ───────────────────────────────────────────────────────────
SEARCH_URL = (
    "https://www.seloger.com/classified-map"
    "?availableFromMax=2027-03-01"
    "&distributionTypes=Buy"
    "&energyCertificate=E,D,C,B,A,F"
    "&estateTypes=House,Apartment"
    "&locations=AD04FR5,AD06FR76"
    "&locationsInBuildingExcluded=Groundfloor"
    "&numberOfBedroomsMax=2&numberOfBedroomsMin=1"
    "&numberOfRoomsMin=2"
    "&priceMax=300000&priceMin=100000"
    "&priceType=Default"
    "&projectTypes=Resale,New_Build,Projected"
    "&spaceMax=60&spaceMin=30"
    "&order=DateDesc"
    "&bbox=Mi4yODAxNjY5NDgxNzUwNjUsNDguODA1MDE5Njk2NDYwOTYsMi44MzQyNDk3NTYyMDMwNjQ0LDQ4LjkzMTcwNjc1ODg2ODU4Ng"
)

# ── API patterns to intercept ─────────────────────────────────────────────────
# SeLoger calls its own API — these patterns catch the listing endpoints.
# If nothing is captured, open DevTools → Network tab on the page and look
# for XHR/fetch calls returning JSON arrays of listings, then add the pattern.
INTERCEPT_PATTERNS = [
    r"api\.seloger\.com",
    r"seloger\.com/api",
    r"seloger\.com/classified",
    r"/classifieds",
    r"/listings",
    r"graphql",
]

captured_responses = []


def matches_any(url: str) -> bool:
    return any(re.search(p, url, re.IGNORECASE) for p in INTERCEPT_PATTERNS)


def extract_listings(data) -> list[dict]:
    """Pull listing records out of whatever shape the API returns."""
    listings = []

    if isinstance(data, list):
        candidates = data
    elif isinstance(data, dict):
        # Try common envelope keys
        for key in ("classifieds", "listings", "items", "results", "data", "hits"):
            if key in data and isinstance(data[key], list):
                candidates = data[key]
                break
        else:
            # GraphQL style: data.someField
            if "data" in data and isinstance(data["data"], dict):
                for v in data["data"].values():
                    if isinstance(v, list):
                        candidates = v
                        break
                else:
                    candidates = [data]
            else:
                candidates = [data]
    else:
        return []

    for item in candidates:
        if not isinstance(item, dict):
            continue
        listing = parse_listing(item)
        if listing:
            listings.append(listing)

    return listings


def parse_listing(item: dict) -> dict | None:
    """Normalize a raw listing dict into a clean flat record."""
    # SeLoger nests data differently depending on the endpoint.
    # This handles the most common shapes — adjust if needed.

    def get(*keys, default=None):
        """Nested get with fallback keys."""
        for key in keys:
            parts = key.split(".")
            val = item
            for p in parts:
                if isinstance(val, dict):
                    val = val.get(p)
                else:
                    val = None
                    break
            if val is not None:
                return val
        return default

    price = get("price", "prices.displayed", "prices.main", "price.value")
    surface = get("surface", "livingArea", "area", "surfaces.surface")
    rooms = get("rooms", "roomsCount", "numberOfRooms")
    bedrooms = get("bedrooms", "bedroomsCount", "numberOfBedrooms")
    city = get("city", "location.city", "address.city", "cityLabel")
    postal_code = get("postalCode", "location.postalCode", "address.postalCode")
    title = get("title", "name", "publicTitle")
    url_path = get("url", "link", "classifiedURL", "permalink")
    listing_id = get("id", "classifiedId", "listingId")
    energy = get("energyClassification", "energyCertificate", "dpe", "energy.letter")
    estate_type = get("estateType", "propertyType", "type")
    date_pub = get("publicationDate", "createdAt", "publishedAt", "date")
    agency = get("agency.name", "contact.name", "agencyName")
    lat = get("coordinates.lat", "location.lat", "latitude")
    lng = get("coordinates.lng", "location.lng", "longitude")

    if not price and not surface:
        return None  # skip non-listing objects

    full_url = (
        f"https://www.seloger.com{url_path}"
        if url_path and url_path.startswith("/")
        else url_path
    )

    return {
        "id": listing_id,
        "title": title,
        "price_eur": price,
        "surface_m2": surface,
        "rooms": rooms,
        "bedrooms": bedrooms,
        "city": city,
        "postal_code": postal_code,
        "energy": energy,
        "type": estate_type,
        "agency": agency,
        "published": date_pub,
        "lat": lat,
        "lng": lng,
        "url": full_url,
        "price_per_m2": round(price / surface, 0) if price and surface else None,
    }


async def intercept_response(response):
    url = response.url
    if not matches_any(url):
        return
    content_type = response.headers.get("content-type", "")
    if "json" not in content_type:
        return
    try:
        body = await response.json()
        listings = extract_listings(body)
        if listings:
            print(f"  ✓ {len(listings)} listings from {url[:80]}...")
            captured_responses.extend(listings)
        else:
            # Still save raw for inspection
            print(f"  · JSON from {url[:80]} — no listings parsed, saving raw")
            with open("seloger_raw_responses.json", "a") as f:
                json.dump({"url": url, "body": body}, f, ensure_ascii=False)
                f.write("\n")
    except Exception as e:
        print(f"  ✗ Could not parse {url[:80]}: {e}")


async def scrape():
    print("Starting SeLoger scraper...")
    print(f"URL: {SEARCH_URL[:80]}...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # Set True to run silently
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1440, "height": 900},
            locale="fr-FR",
        )

        page = await context.new_page()
        page.on("response", lambda r: asyncio.create_task(intercept_response(r)))

        print("\nNavigating to SeLoger...")
        await page.goto(SEARCH_URL, wait_until="networkidle", timeout=30000)

        # Let the map and listings fully load
        print("Waiting for listings to load...")
        await page.wait_for_timeout(4000)

        # Scroll to trigger lazy-loaded content
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)

        # If the page has a cookie banner, dismiss it
        try:
            await page.click("button[id*='accept'], button[id*='cookie']", timeout=2000)
        except Exception:
            pass

        await browser.close()

    print(f"\n{'─'*50}")
    print(f"Total listings captured: {len(captured_responses)}")

    if not captured_responses:
        print("\n⚠ No listings captured.")
        print("Open seloger_raw_responses.json to inspect what the API returned.")
        print("Look for the listing data structure and update parse_listing() accordingly.")
        return

    # Deduplicate by id
    seen = set()
    unique = []
    for l in captured_responses:
        key = l.get("id") or l.get("url") or str(l)
        if key not in seen:
            seen.add(key)
            unique.append(l)

    print(f"Unique listings after dedup: {len(unique)}")

    # Save JSON
    json_path = f"seloger_listings_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"→ JSON: {json_path}")

    # Save CSV
    df = pd.DataFrame(unique)
    df = df.sort_values("price_eur", ascending=True)
    csv_path = json_path.replace(".json", ".csv")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"→ CSV:  {csv_path}")

    # Quick summary
    print(f"\nPrice range: {df['price_eur'].min():,.0f} – {df['price_eur'].max():,.0f} €")
    print(f"Surface range: {df['surface_m2'].min()} – {df['surface_m2'].max()} m²")
    if df['price_per_m2'].notna().any():
        print(f"Price/m²: {df['price_per_m2'].min():,.0f} – {df['price_per_m2'].max():,.0f} €/m²")


if __name__ == "__main__":
    asyncio.run(scrape())
