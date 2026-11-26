# Local Keycloak development environment

This environment is for local integration and developer testing only. It is not a production identity deployment.

## Start the services

1. Copy `.env.example` to `.env`.
2. Change `KEYCLOAK_ADMIN_PASSWORD` to a strong local password before starting.
3. Start Docker Desktop (or another Docker Engine with Compose).
4. Run:

```bash
docker compose up -d postgres keycloak
docker compose ps
```

Keycloak is available at:
- Admin console: http://localhost:8081/admin/
- Realm issuer: http://localhost:8081/realms/trade-intelligence
- OpenID discovery: http://localhost:8081/realms/trade-intelligence/.well-known/openid-configuration
- JWKS: http://localhost:8081/realms/trade-intelligence/protocol/openid-connect/certs

The realm import creates realm `trade-intelligence`, API audience/client `trade-api`, local token client `trade-api-dev-cli`, ten explicit realm roles, and an audience mapper that adds `trade-api` to access-token audience claims.

The token client is a public client with direct-access grants enabled solely to make local password-grant testing straightforward. Do not copy this flow into production. Production clients should use an appropriate OAuth 2.0 flow such as Authorization Code with PKCE for users, and should disable password grants.

## Create a local test user

1. Sign in to the Keycloak admin console using the local bootstrap administrator credentials.
2. Select the `trade-intelligence` realm.
3. Open **Users → Add user** and create a non-production test user.
4. Set a local test password under **Credentials** and turn off **Temporary**.
5. Open **Role mapping → Assign role** and assign one of the explicitly scoped roles: `rule-set-reader`, `rule-set-author`, `rule-set-validator`, `rule-set-publisher`, `rule-set-activator`, `trade-admin`, `scenario-creator`, `scenario-evaluator`, `authority-endpoint-verifier`, or `source-catalog-author`. Assign only the role needed for the test. `trade-admin` grants rule-set lifecycle permissions only; it does not inherit data-domain mutation permissions.
6. Do not reuse a real staff account or password.

## Obtain a local access token

Set `KEYCLOAK_TEST_USERNAME` and `KEYCLOAK_TEST_PASSWORD` in your terminal for the local test user. Do not commit these values or paste a live token into source control.

PowerShell example:

```powershell
$tokenResponse = Invoke-RestMethod -Method Post `
  -Uri "http://localhost:8081/realms/trade-intelligence/protocol/openid-connect/token" `
  -ContentType "application/x-www-form-urlencoded" `
  -Body @{
    grant_type = "password"
    client_id = "trade-api-dev-cli"
    username = $env:KEYCLOAK_TEST_USERNAME
    password = $env:KEYCLOAK_TEST_PASSWORD
  }

$env:KEYCLOAK_TEST_ACCESS_TOKEN = $tokenResponse.access_token
```

The application verifier should be configured with:
- `KEYCLOAK_ISSUER=http://localhost:8081/realms/trade-intelligence`
- `KEYCLOAK_AUDIENCE=trade-api`
- `KEYCLOAK_ROLE_CLIENT_ID=trade-api`

The verifier must accept a valid access token, reject an ID token, and reject invalid signatures, issuer, audience, expiry, or token type. Unknown realm roles must grant no permissions.

## Run the live integration test

After creating the test user and setting the local environment variables, run:

```bash
pytest tests/integration/test_keycloak_live.py -q
```

On PowerShell, set the two variables with `$env:KEYCLOAK_TEST_USERNAME` and `$env:KEYCLOAK_TEST_PASSWORD` before running pytest.

## Important security boundary

- The local bootstrap credentials are for development only.
- The password grant is for local smoke testing only.
- Do not expose Keycloak's development HTTP endpoint to a public network.
- Do not reuse local credentials in production.
- Do not commit `.env`, passwords, access tokens, client secrets, or signing keys.
- The six legacy data-domain mutation routes remain registered but fail closed with HTTP 503; their handlers do not execute. Do not remove this lock until live authentication, per-operation authorization, audit persistence, database privileges, and deployment controls have been reviewed.
- Rule-set administrative write routes remain unregistered pending their own verified authorization and operational controls.
- The data-domain roles are defined in the realm export but are not assigned to any users by default. `scenario-creator` grants only `scenario:create`; `scenario-evaluator` grants only `scenario:evaluate`; `authority-endpoint-verifier` grants only `authority_endpoint:verify`; and `source-catalog-author` grants `source:create`, `document:create`, and `provision:create`.
