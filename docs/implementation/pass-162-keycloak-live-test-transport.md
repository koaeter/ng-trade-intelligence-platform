# Pass 162 — Secure transport for live Keycloak verification

## Change

The opt-in live Keycloak integration test now validates the configured issuer URL before sending test-user credentials.

- Remote Keycloak endpoints must use HTTPS.
- Plain HTTP is permitted only for loopback development addresses (`localhost`, `127.0.0.1`, or `::1`).
- Non-HTTP(S) schemes and URLs without a hostname are rejected.
- The transport guard is unit-tested without contacting an identity provider.

This allows the same test to target either the local Compose realm or a controlled remote test realm without sending passwords over public plaintext HTTP.

## Scope and security boundary

This is a client-side test safeguard, not a substitute for TLS certificate validation, production ingress configuration, secret management, or a live identity-provider test. The test still requires explicitly supplied test credentials and remains opt-in.

The six legacy data-domain mutation routes remain locked with HTTP 503. No administrative route is enabled by this pass.

## Verification

The new transport cases run as part of the normal test suite. A skipped live Keycloak test does not establish that a real token, issuer, audience, JWKS key, or role assignment has been verified.
