# Mutation audit-log deployment requirements

## Current implementation boundary

The API emits payload-free JSON audit events through the Python logger named
`ng_trade_intelligence.security.audit`. The event is suitable for a structured
logging handler, but the application does not currently configure a durable
audit store, central collector, retention policy, immutable archive, alerting
rule, or log-integrity mechanism.

The repository's current `docker-compose.yml` is a local development stack for
PostgreSQL and Keycloak. It does not define a production API deployment or an
audit-log collection service. Do not treat local console output or a successful
HTTP 503 response as proof that an event has been durably retained.

## Deployment acceptance requirements

Before any mutation route can be considered for re-enablement, the deployment
owner must demonstrate all of the following:

1. **Collection:** application audit events are captured from the API process
   and delivered to an approved central logging or audit service. Delivery must
   be monitored, and dropped or rejected events must raise an operational
   alert.
2. **Durability:** the approved sink acknowledges persistence before the
   deployment is considered audit-ready. The organization must define how the
   system behaves during sink outages; mutation requests must remain denied
   while the current lock is active.
3. **Integrity:** retained events are protected against unauthorized alteration
   and deletion. Use the organization's approved immutable/WORM or equivalent
   integrity controls where required.
4. **Access control:** access to audit events is restricted to authorized
   operational, security, audit, and investigation roles, with access itself
   logged where supported.
5. **Retention:** the records owner must set a retention and disposal schedule
   consistent with applicable Nigerian public-sector records, legal-hold,
   security, and privacy requirements. This repository intentionally does not
   guess a retention period.
6. **Availability and recovery:** retention, backup, restoration, and
   continuity procedures are documented and periodically tested.
7. **Redaction:** request bodies, authorization headers, cookies, query strings,
   client IP addresses, passwords, access tokens, and caller-controlled values
   remain excluded unless a separately approved and privacy-reviewed policy
   explicitly requires a field.
8. **Operational monitoring:** alert on collection failure, unexpected changes
   to the event schema, unusual blocked-write volume, and retention or storage
   capacity approaching limits.
9. **Verification:** deployment tests demonstrate that an emitted event reaches
   the approved sink, can be retrieved by an authorized investigator, and is
   protected by the required retention and integrity controls.

## Event contract

The current blocked-mutation event contains only:

- `event`
- `method`
- `route` (registered route template, not a caller-provided path value)
- `outcome`
- `reason`
- `http_status`
- `actor` (`unverified` until identity has actually been verified)

Changes to this schema require corresponding regression tests and a security
review. Do not add raw request data or credentials to improve searchability.

## Re-enablement gate

The six legacy mutation routes remain blocked with HTTP 503. Passing unit tests
or seeing an audit message in a development console does not satisfy this
deployment gate. Re-enablement requires verified live Keycloak authentication,
per-operation authorization tests, durable audit delivery and retention
evidence, database privilege review, and an explicit approval of the permission
matrix and deployment controls.
