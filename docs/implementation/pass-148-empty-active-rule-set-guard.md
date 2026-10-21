# Pass 148 — Fail closed on an empty active rule set

## Objective

Prevent the canonical evaluation endpoint from silently returning an empty result set when the active rule set has no memberships.

## Finding

The initial database migration seeds an `ACTIVE` rule-set version named `initial`, but it does not seed requirement memberships. After the API moves to revision-aware evaluation, that empty active rule set would otherwise cause evaluation to return an empty list without explaining why.

## Implemented

- The revision-aware service now rejects an active rule set with no requirement memberships.
- The API maps this configuration condition to HTTP 409 Conflict rather than returning a successful empty evaluation.
- A unit test verifies the service fails closed when the active rule set is empty.
- The initial seed remains unchanged; legacy requirements are not automatically treated as immutable revisions or inserted into a rule set without validation.

## Operational implication

Before evaluation can produce results in a newly migrated environment, an administrator must author a rule set containing valid requirement revisions, validate it, publish it, and activate it. This avoids silently treating an empty versioned scope as if no requirements applied.

## Verification status

GitHub Actions has been running on recent commits, but repository-wide Ruff failures have prevented type-check and test steps from running. Confirm the workflow state before treating this change as CI-verified.

## Next

Inspect the migration and rule-set activation invariants, especially whether the database should enforce at most one active rule set and whether legacy data needs a deliberate, validated conversion into immutable revisions.
