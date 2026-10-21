# Pass 149 — Administrative security boundary and lifecycle hardening

## Decision

Develop the rule-set lifecycle and the administrative security boundary in parallel. Lifecycle use cases remain internal application services until a real authentication and authorization mechanism is configured. Do not expose rule-set write endpoints as anonymous API routes.

## Administrative capabilities

The administrative API must enforce permissions at the application boundary, not merely hide UI controls:

- `rule_set:draft:create` — create a draft from immutable requirement revision IDs.
- `rule_set:validate` — run publication validation and mark a draft validated.
- `rule_set:publish` — publish only a validated rule set.
- `rule_set:activate` — revalidate immediately before activation, then switch the active version.
- `rule_set:read` — inspect versions, memberships, validation status, and activation history.

Recommended separation of duties: authoring, validation, and activation should be separately assignable permissions. A production deployment can require an approver distinct from the author before activation. All write operations must record the authenticated principal, timestamp, target version, action, and outcome in an append-only audit record.

## Authentication integration boundary

The repository currently has no established user identity, role, or token-validation system. Implementing a homemade token scheme or exposing endpoints with a placeholder dependency would create a false sense of security. Therefore, this pass defines the contract but deliberately does not expose administrative HTTP write endpoints.

Before exposing them, choose and configure an identity provider/protocol (prefer an established OIDC/OAuth2 provider), validate issuer, audience, signature, expiry, and relevant scopes/roles, and map the authenticated identity to the permissions above. Fail closed if identity or permissions cannot be established. Do not use a shared static admin secret as the long-term identity and audit model.

## Lifecycle hardening implemented

- Validation and activation now fail closed if the publication validator has not been configured.
- Activation revalidates the rule set immediately before switching active versions.
- Failed validation leaves the target status unchanged; failed activation does not retire the currently active version.
- Draft authoring rejects duplicate revision IDs and multiple revisions for the same requirement before writing any records.
- Publication remains restricted to validated versions.
- The existing database session owns the transaction; the API must commit only after the whole operation succeeds and roll back on exceptions.

## Concurrency caveat

The current activation sequence reads the active version and then performs status updates. It is safe within a single ordinary transaction but has not yet been proven race-safe under simultaneous activations. Before production activation endpoints are enabled, add database-enforced single-active semantics and concurrency/integration tests for competing activation requests. The initial migration's empty active seed also requires an explicit validated migration or replacement workflow rather than implicit legacy conversion.

## Next

Implement and test a repository-level atomic activation operation (including database uniqueness/locking strategy), then add audit events to the application lifecycle. Once those contracts are in place, wire the operations to an authenticated admin dependency after the identity-provider choice is explicit.
