---
name: api-documentation
description: Document REST APIs in OpenAPI 3.0 format — endpoint descriptions, request/response schemas, auth requirements, and realistic examples. Use when adding new endpoints or when existing API documentation is missing or outdated.
argument-hint: "path/to/controller or route file"
---

> **Using skill api-documentation.**

# API Documentation

Produce complete, accurate REST API documentation. Generates OpenAPI 3.0 specs, endpoint descriptions, and example payloads.

**Freedom level: MEDIUM** — enforces the documentation checklist strictly (LOW); names, descriptions, and examples use judgment (MEDIUM).

## How to Use

Provide the controller/route code. Specify the output format: OpenAPI YAML, inline code comments, or markdown docs.

## Documentation Checklist

For each endpoint, document:

- [ ] HTTP method and path
- [ ] Summary (one line) and description (detailed)
- [ ] All path parameters with type and constraints
- [ ] All query parameters (required vs optional)
- [ ] Request body schema with all fields described
- [ ] All response codes (200, 201, 400, 401, 403, 404, 500) with schemas
- [ ] Authentication requirement (`bearerAuth` or `apiKey`)
- [ ] At least one request example and one response example

## OpenAPI Standards

### Endpoint Names
Use action-oriented `operationId`s: `createUser`, `getUserById`, `updateOrderStatus` — not `usersPost` or `getUser1`.

### Schema Design
- Use `$ref` to reuse schemas — do not inline the same schema in multiple places
- Mark required fields explicitly in the `required:` array
- Add `description` to every property
- Use `format` where applicable: `date-time`, `uuid`, `email`, `uri`

### Examples
Include realistic but fictional data:
- Emails: `alice.dupont@example.com`
- Dates: `2024-01-15T10:30:00Z`
- IDs: UUID v4 format
- Names: neutral fictional names

## Template

See `references/openapi-endpoint.yaml` for a complete endpoint template.
