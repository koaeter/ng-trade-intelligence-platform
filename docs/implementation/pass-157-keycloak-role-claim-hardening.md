# Pass 157 — Fail-closed Keycloak role-claim validation

## Delivered

- Tightened access-token claim parsing in `infrastructure/security/keycloak.py`.
- Rejects a present `realm_access` claim unless it is an object, and rejects its `roles` member unless it is a list of strings.
- Rejects a present `resource_access` claim unless it is an object.
- Rejects the configured API client's role entry unless it is an object, and rejects its `roles` member unless it is a list of strings.
- Preserves compatibility with valid tokens that omit optional role containers; such tokens authenticate with an empty permission set and therefore cannot pass a permission check.
- Added regression coverage for malformed realm and client role structures and for tokens with no optional role claims.

## Security rationale

Previously, malformed outer role-claim containers could be treated like absent claims. Although this did not grant permissions, silently normalizing malformed authorization data obscured token-shape errors and made the authorization boundary less explicit.

The verifier now distinguishes:
- absent optional role claims: valid identity, zero permissions;
- well-formed role claims: only explicitly allow-listed roles map to permissions;
- malformed role claims: reject the token as untrusted.

Unknown but well-formed role names continue to grant no permissions.

## Verification

The new tests are included in the existing scoped CI Ruff gate and full pytest job. CI results must be checked after the commits; this implementation note does not claim a passing run until GitHub Actions reports success.

## Unchanged security boundary

No administrative write routes were registered or exposed in this pass. Live Keycloak verification remains pending a running Keycloak realm and dedicated test user.
