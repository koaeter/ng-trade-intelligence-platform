# Pass 156 — Local Keycloak development environment

## Delivered

- Added Keycloak 26.2.5 to the existing Docker Compose environment on host port 8081; the existing PostgreSQL service remains available unchanged.
- Added an importable `trade-intelligence` realm with explicit realm roles matching the application's permission allow-list.
- Added the `trade-api` resource-server audience and a local-only public client `trade-api-dev-cli` for obtaining test access tokens.
- Added an audience mapper so locally issued access tokens include `trade-api`.
- Updated `.env.example` with local issuer, audience, and bootstrap administrator settings.
- Added local setup, test-user creation, token acquisition, and security guidance in `docs/security/local-keycloak-development.md`.
- Added an opt-in live integration test. It skips in CI unless a Keycloak issuer and dedicated local test-user credentials are supplied; when enabled, it obtains an access token from Keycloak and verifies it through the production token-verifier implementation.
- Added the live integration test to the scoped Ruff gate.

## Local operation

The developer starts the services with Docker Compose, creates a dedicated test user in the imported realm, assigns a least-privilege realm role, and runs the opt-in integration test. No live Keycloak credentials, access tokens, or signing keys are stored in the repository.

## Security decisions

- Password-grant use is limited to this isolated local smoke-test client. It is not a production authentication recommendation.
- The API client remains a bearer-only resource server.
- The local realm is HTTP-only and must not be exposed to public networks.
- Production realm, audience, role assignment, TLS, and client-flow configuration remain deployment-specific.
- Administrative write routes remain unregistered until a live identity-provider test and security review are complete.

## Verification boundary

The repository can validate the realm import structure and application verifier in CI, but the actual Keycloak container has not been started in this hosted development session. The live test must be run on a machine with Docker Compose and the local test user configured. Do not treat local environment preparation as proof of production readiness.
