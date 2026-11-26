# Keycloak deployment checklist

This checklist prepares the identity-provider configuration for the administrative API. It does not authorise enabling administrative write routes. The route exposure gate remains closed until a real deployment has passed the verification steps below.

## Realm and API client

- Create or select the dedicated trade-intelligence realm.
- Register the API as a resource-server client, using a stable client identifier.
- Configure the access-token audience so the issued access token contains the exact value configured as `KEYCLOAK_AUDIENCE`.
- Use HTTPS for the issuer and JWKS endpoint in deployed environments.
- Configure RS256 signing for the realm's access tokens.
- Ensure the access-token payload contains `typ=Bearer`; ID tokens must not be accepted by this API.

## Role claims

The verifier reads roles from both supported Keycloak claim locations:

- Realm roles: `realm_access.roles`
- Client roles: `resource_access[KEYCLOAK_ROLE_CLIENT_ID].roles`

Assign only the application roles that are explicitly mapped in `infrastructure/security/keycloak.py`:

- `trade-admin`
- `rule-set-reader`
- `rule-set-author`
- `rule-set-validator`
- `rule-set-publisher`
- `rule-set-activator`
- `scenario-creator`
- `scenario-evaluator`
- `authority-endpoint-verifier`
- `source-catalog-author`

Unknown roles grant no application permissions. Do not create a broad wildcard mapping.

## Application environment

Set these deployment values from the actual realm/client configuration:

- `KEYCLOAK_ISSUER`: exact realm issuer URL, ending in `/realms/{realm}`
- `KEYCLOAK_AUDIENCE`: audience expected by this API
- `KEYCLOAK_JWKS_URL`: optional override; otherwise derived from the issuer
- `KEYCLOAK_ROLE_CLIENT_ID`: optional client ID when client roles are used; defaults to the audience

No client secret is required for local JWT signature verification. Never place signing private keys or client secrets in source control.

## Verification before route exposure

1. Obtain an access token from the deployed realm and inspect its issuer, audience, token type, subject, and role claim locations.
2. Verify the token through the application verifier using the live JWKS endpoint.
3. Verify a token with the wrong issuer, audience, signature, expiry, or token type is rejected.
4. Verify each role receives only its intended permissions and unknown roles receive none.
5. Verify unauthenticated requests receive HTTP 401 and authenticated but underprivileged requests receive HTTP 403.
6. Verify successful and failed lifecycle operations produce the expected audit events.
7. Verify the application database role cannot update or delete audit events outside the approved retention/administrative process.
8. Obtain a deployment/security review before enabling any administrative write route.

Until all checks are complete, keep the six legacy data-domain mutation routes locked with HTTP 503 and do not register new administrative write routes. The legacy routes remain registered for compatibility, but their fail-closed dependency prevents their handlers from executing. The `trade-admin` role is limited to rule-set lifecycle permissions and does not inherit data-domain permissions.
