# Pass 151 — Keycloak token verification boundary

## Implemented

- Added a Keycloak-compatible OIDC access-token verifier at `infrastructure/security/keycloak.py`.
- Verifies RS256 signatures using Keycloak's JWKS endpoint, issuer, audience, expiry, issued-at and subject claims.
- Maps only explicit, recognized Keycloak realm/client roles to application permissions. Unknown roles grant no permissions.
- Added tests for role mapping, invalid-token rejection, blank tokens and missing issuer/audience configuration.
- Added runtime dependency `PyJWT[crypto]` and documented environment variables in `.env.example`.

## Security constraints

- This is a verifier component, not an enabled administrative API.
- No administrative write routes are registered by this pass.
- Configure `KEYCLOAK_ISSUER` as the exact realm issuer URL and `KEYCLOAK_AUDIENCE` as the API audience expected in access tokens. Configure Keycloak client roles or realm roles using the documented role names.
- The default role map is intentionally allow-listed. Assign roles through Keycloak administration and test the issued access token's actual claims before deployment.
- JWKS retrieval depends on the configured identity endpoint being reachable. Authentication must fail closed if signing keys cannot be resolved or token claims do not validate.
- Production deployment still requires HTTPS, appropriate token lifetime/key-rotation configuration, secret/configuration management, and integration tests against a real Keycloak realm.

## Not yet enabled

Administrative write endpoints remain unexposed. Before route wiring, verify real token validation, issuer/audience alignment, role claims, 401/403 behavior, and application permission enforcement in the deployment environment. A valid token without an allowed role must not receive write permissions.

## Rule-set lifecycle continuation

Continue with append-only lifecycle audit events and tests that bind actor, operation, target rule-set version, timestamp, and outcome to the same transaction as successful state changes. Failed validation or activation must not produce a successful-transition audit record.
