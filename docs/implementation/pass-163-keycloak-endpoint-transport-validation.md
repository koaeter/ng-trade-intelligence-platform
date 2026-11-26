# Pass 163 — Runtime validation of Keycloak identity endpoints

## Change

The Keycloak token verifier now validates both its configured issuer and JWKS endpoint before constructing the JWKS client.

- Remote identity endpoints must use HTTPS.
- HTTP is allowed only for loopback development endpoints (`localhost`, `127.0.0.1`, and `::1`).
- URLs must have a hostname and use HTTP or HTTPS.
- URLs containing embedded credentials, query parameters, or fragments are rejected.
- Both the issuer and an explicitly overridden JWKS URL are checked.

The verifier raises `KeycloakConfigurationError` for invalid endpoint configuration, failing closed before token verification begins.

## Tests

Unit tests cover remote plaintext HTTP, an insecure overridden JWKS URL, embedded URL credentials, query strings, and malformed URLs. Existing local loopback and HTTPS test configurations remain supported.

## Operational boundary

This protects the application's configured identity-provider endpoints from accidental insecure transport. It does not configure TLS, validate deployment DNS, or replace certificate verification performed by the HTTP client.

The six legacy data-domain mutation endpoints remain disabled with HTTP 503. No live Keycloak instance was contacted and no route was unlocked.
