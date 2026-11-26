# Local Keycloak live-test permission assertions

The opt-in `tests/integration/test_keycloak_live.py` test can assert both permissions that a real token must contain and permissions it must not contain. This is useful for checking least-privilege role mappings against a live Keycloak realm rather than relying only on unit-test fixtures.

Configure the following optional environment variables before running the test:

- `KEYCLOAK_TEST_CLIENT_ID` — defaults to `trade-api-dev-cli`.
- `KEYCLOAK_TEST_EXPECTED_PERMISSIONS` — comma-separated permissions that must be present. Defaults to `rule_set:read` for the existing reader smoke test.
- `KEYCLOAK_TEST_FORBIDDEN_PERMISSIONS` — comma-separated permissions that must be absent.

For a user assigned only `trade-admin`, a PowerShell example is:

```powershell
$env:KEYCLOAK_TEST_EXPECTED_PERMISSIONS = "rule_set:read,rule_set:draft:create,rule_set:validate,rule_set:publish,rule_set:activate"
$env:KEYCLOAK_TEST_FORBIDDEN_PERMISSIONS = "scenario:create,scenario:evaluate,authority_endpoint:verify,source:create,document:create,provision:create"
pytest tests/integration/test_keycloak_live.py -q
```

For a user assigned only `scenario-creator`, set expected permissions to `scenario:create` and forbidden permissions to the other five data-domain permissions plus the rule-set write permissions that the role should not grant. Repeat with a separate test user for each role. Do not combine roles on the same user when verifying the isolation of an individual role.

These tests require a running Keycloak realm and a non-production test account. They are intentionally skipped when issuer or test credentials are absent. A skipped test is not evidence of live authentication verification.
