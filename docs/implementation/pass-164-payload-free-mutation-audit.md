# Pass 164 — Payload-free audit events for blocked mutations

## Change

Every request reaching one of the six temporarily disabled mutation routes now emits a structured warning-level security audit event before the API returns HTTP 503.

The event records only:

- event type: `mutation_blocked`
- HTTP method
- registered route template
- outcome: `denied`
- reason: `keycloak_verification_pending`
- HTTP status: `503`
- actor classification: `unauthenticated`

The audit helper deliberately excludes request bodies, authorization headers, cookies, query strings, caller-supplied identifiers, and client IP addresses. It does not create a database dependency or alter the route's fail-closed behavior.

## Tests

The API regression test now asserts that all six blocked mutation requests:

1. Continue to return HTTP 503 with the existing response detail.
2. Emit one structured audit record each.
3. Record the registered route template and denial outcome.
4. Do not include the test provision payload in the audit message.

The read-only health endpoint remains available.

## Operational limitation

These events are emitted through Python's standard logging system. Durable retention, centralized collection, access controls, alerting, and log-integrity guarantees depend on the eventual deployment logging pipeline. This pass does not claim tamper-evident or database-backed audit storage.

## Security boundary

All six mutation routes remain disabled. No mutation handler is executed, no data is changed, and no route is unlocked. Live Keycloak verification is still outstanding.
