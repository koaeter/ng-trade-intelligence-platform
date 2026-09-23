# Pass 52 — Rule-set versioning

## Objective

Remove the deterministic evaluator's dependence on an application-code constant for historical rule-set identity.

## Implemented

- Added immutable RuleSetVersion domain data.
- Added ACTIVE/RETIRED lifecycle state.
- Added a persisted rule_set_versions table.
- Added an initial seeded rule-set version.
- Added a repository boundary for resolving the active version.

## Governance

Application software versions and domain rule-set versions are separate concepts.

A software deployment can change without changing the legal rule set, and a rule set can change without requiring the domain model itself to change.

## Next

The next pass should connect the evaluator/orchestrator to the persisted active rule-set version and establish version transition validation.
