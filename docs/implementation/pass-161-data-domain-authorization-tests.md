# Pass 161 — Data-domain authorization dependency coverage

## Scope

This pass strengthens the authorization adapter's tests without registering or unlocking any mutation route.

## Permission checks

The FastAPI permission dependency is tested for every data-domain permission introduced in Pass 160:

- `scenario:create`
- `scenario:evaluate`
- `authority_endpoint:verify`
- `source:create`
- `document:create`
- `provision:create`

For each permission, tests prove both outcomes:

1. A principal carrying that exact permission is accepted.
2. An authenticated principal without that exact permission receives HTTP 403.

This verifies exact permission matching and guards against accidental broad access. Authentication failures remain HTTP 401, while authorization failures remain HTTP 403.

## Route security boundary

All six legacy mutation routes remain registered but blocked by the Pass 159 fail-closed dependency. Their route-level response tests continue to require HTTP 503, and the route inventory test prevents unreviewed mutation routes from being added.

The new dependency tests do not constitute live Keycloak verification. They exercise the application authorization boundary with validated-principal test fixtures; they do not verify a real Keycloak-issued token or role assignment.

## Verification still required before unlocking routes

- Run the opt-in live Keycloak integration test against the local realm.
- Verify each data-domain role using a real signed access token.
- Verify `trade-admin` receives no data-domain permission in a live token.
- Review audit persistence and failure-path behaviour for each mutation.
- Confirm production identity-client configuration and deployment controls.

No mutation route is re-enabled in this pass.
