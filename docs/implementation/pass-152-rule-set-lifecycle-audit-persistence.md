# Pass 152 — Rule-set lifecycle audit persistence

## Implemented

- Added migration `0038_rule_set_audit_events.py`, chained after migration 0037.
- Added `RuleSetAuditEventModel` with actor subject, operation, target version, outcome, timestamp, and optional detail.
- Added `SqlAlchemyRuleSetAuditRepository` with a constrained action/outcome vocabulary, required actor identity, insert-only API, and target history query.
- Added unit coverage for event persistence and invalid metadata.
- Added a transaction test showing that a successful activation state change and its audit record roll back together when they use the same SQLAlchemy session and transaction.

## Important integrity boundary

The repository deliberately offers no update/delete methods for audit events, but application-level API shape alone is not a tamper-proof audit guarantee. Database privileges and operational controls must prevent ordinary application principals from updating or deleting audit rows; a separate privileged migration/maintenance role may still be required. Consider external log shipping or immutable storage for higher assurance.

The rule-set application service now optionally records successful validate, publish, and activate events when an audit repository and actor subject are supplied. Both repositories must share one session and transaction; if audit insertion fails, the caller must roll back rather than commit the state change. Missing actor identity is rejected before mutation. Failed-attempt logging is still separate work: it needs a durable transaction after the failed operation rolls back, so a rejected validation does not erase its own audit record.

## Security rollout gate

Administrative write routes remain disabled. Keycloak role mapping and dependencies exist, but real-realm integration, production configuration, CI tests, and database privilege validation are still required before route registration.
