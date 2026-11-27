# Pass 166 — Accurate audit actor classification

## Finding

The mutation lock deliberately does not authenticate requests or inspect authorization headers. Therefore, an audit field that labels every blocked caller as `unauthenticated` would claim more than the system has established: a request may contain a bearer token, but its identity and permissions have not been verified.

## Change

Blocked-mutation audit events now record:

- `actor: "unverified"`

This means the caller identity has not been established by the API. It does not assert that credentials were absent or invalid. The event continues to omit authorization headers, cookies, query strings, request bodies, and caller-controlled identifiers.

## Regression coverage

The all-routes audit test now asserts the `unverified` actor classification alongside the existing payload-free event schema and 503 response checks.

## Security boundary

No authentication or authorization behavior is enabled by this change. The six legacy mutation endpoints remain blocked pending live Keycloak verification and the established authorization and operational gates.
