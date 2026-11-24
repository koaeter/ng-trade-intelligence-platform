# Pass 158 — API mutation-route security inventory

## Scope

Audited the FastAPI application route registrations in `apps/api/main.py` and classified every currently registered HTTP mutation method.

## Findings

The API currently registers six POST operations:

| Method | Route | Effect |
|---|---|---|
| POST | `/api/v1/export-scenarios` | Creates an export scenario |
| POST | `/api/v1/export-scenarios/{scenario_id}/evaluate` | Runs and persists scenario evaluations |
| POST | `/api/v1/authority-endpoints/{endpoint_id}/verify` | Performs endpoint verification and persists its result |
| POST | `/api/v1/sources` | Registers a source |
| POST | `/api/v1/documents` | Creates a document |
| POST | `/api/v1/provisions` | Creates a provision |

No PUT, PATCH, or DELETE route was found in the application route registrations.

## Security assessment

These six operations mutate persistent state or trigger a state-changing workflow. They are not part of the rule-set administrative route family covered by the existing route-exposure regression test.

The current handlers do not declare a Keycloak principal or permission dependency. Therefore, the API's existing rule-set write-route restriction must not be mistaken for a global write-access restriction.

The six routes are classified as **legacy unauthenticated mutation routes pending remediation**. This pass does not silently change their behaviour or remove them because that would be a breaking API/product decision.

## Regression protection

Added `tests/api/test_mutation_route_inventory.py`, which asserts the complete current mutation-route set. Any newly added POST, PUT, PATCH, or DELETE route must now trigger an explicit inventory update and security review.

## Required policy decision before enabling writes

Before these routes are made available for production use, decide whether all six should be disabled until live Keycloak authentication and authorization are verified, or whether a limited subset has a documented trusted deployment boundary.

Recommended secure default: keep all six unavailable to untrusted callers until their permission requirements, audit behaviour, and live Keycloak verification are complete. Route-specific permission mapping should be designed before wiring dependencies:
- scenario creation: a dedicated scenario-create permission;
- scenario evaluation: a dedicated evaluation-run permission;
- endpoint verification: source/authority endpoint management permission;
- source/document/provision creation: source-catalog authoring permission.

Do not reuse the rule-set author role for unrelated data domains.

## Verification status

The inventory test is added to the full pytest suite. CI must be checked after commit. This audit does not claim that the existing mutation routes are protected.
