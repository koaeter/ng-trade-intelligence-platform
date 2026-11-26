# Pass 160 — Least-privilege data-domain role model

## Decision

The owner accepted the recommendation that `trade-admin` must not inherit permissions for data-domain mutations. It remains scoped to the existing rule-set lifecycle permission set.

## Explicit data-domain roles

| Keycloak realm role | Permission(s) | Intended operation |
|---|---|---|
| `scenario-creator` | `scenario:create` | Create an export scenario |
| `scenario-evaluator` | `scenario:evaluate` | Run and persist a scenario evaluation |
| `authority-endpoint-verifier` | `authority_endpoint:verify` | Verify an authority endpoint |
| `source-catalog-author` | `source:create`, `document:create`, `provision:create` | Create source, document, and provision records |

The source-catalog role groups three closely related catalog-authoring operations. The other operations remain separately assignable. No role is assigned to a user by the realm export.

## Non-inheritance guarantee

`trade-admin` continues to grant only:

- `rule_set:read`
- `rule_set:draft:create`
- `rule_set:validate`
- `rule_set:publish`
- `rule_set:activate`

It does not grant scenario, authority-endpoint, source, document, or provision permissions. Unknown roles continue to grant no permissions. The verifier still maps only explicitly allow-listed role names.

## Security boundary retained

This pass changes role definitions and token-to-permission mapping only. It does not attach Keycloak dependencies to the six legacy mutation routes and does not remove the Pass 159 HTTP 503 lock. No data-domain mutation endpoint is re-enabled.

Before any route is protected and unlocked, the project still requires a live Keycloak verification run, positive and negative authorization tests for each operation, audit/failure-path review, and an explicit owner-approved role assignment policy. In particular, the shared `source-catalog-author` role must be confirmed as appropriate for all three catalog operations before route-level authorization is wired.

## Verification

Unit tests cover each new role mapping and explicitly assert that `trade-admin` receives none of the six data-domain permissions. The realm-export test asserts the complete set of defined roles. CI status is recorded only after the corresponding workflow run completes.
