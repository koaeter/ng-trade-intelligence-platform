# Pass 165 — Pre-validation guard for locked mutation routes

## Change

The six legacy mutation routes are now intercepted by HTTP middleware before FastAPI parses or validates request bodies. The middleware matches the request against the registered route table and the explicit locked-route inventory, then:

1. Emits the existing payload-free `mutation_blocked` JSON audit event.
2. Returns HTTP 503 with the established `MUTATIONS_DISABLED_DETAIL` response.
3. Does not call the route handler or read the request body.

The route-level fail-closed dependencies remain in place as a second guard if a locked route is invoked through a code path that does not pass through the application middleware.

Only these six explicit route keys are intercepted:

- `POST /api/v1/export-scenarios`
- `POST /api/v1/export-scenarios/{scenario_id}/evaluate`
- `POST /api/v1/authority-endpoints/{endpoint_id}/verify`
- `POST /api/v1/sources`
- `POST /api/v1/documents`
- `POST /api/v1/provisions`

The middleware does not block read-only routes. The route inventory regression test continues to fail when an unreviewed write route is added.

## Regression coverage

The API tests now also submit:
- Malformed JSON to a locked source-creation route.
- Valid JSON with a structurally invalid body to a locked document-creation route.

Both must return HTTP 503 rather than a JSON parsing or Pydantic validation response, and each request must emit exactly one audit event. Existing tests continue to check all six routes, payload/query/header redaction, and the health endpoint.

## Security boundary

No mutation handler is executed and no data is changed. This does not implement authenticated mutation access, durable audit storage, or live Keycloak verification. All six routes remain disabled until the existing Keycloak, permission, audit persistence, and deployment review gates have been satisfied.
