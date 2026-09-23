# Pass 58 — Rule-set publication validation

## Objective

Prevent an incomplete rule-set from becoming active.

## Implemented

Before publication/activation, a rule-set can now be validated for:
- non-empty requirement membership
- existing immutable requirement revisions
- membership/revision identity consistency
- resolvable product references
- resolvable HS references
- resolvable origin/destination references
- structurally valid revision-bound rule trees

## Governance effect

Rule-set activation is no longer just a status change. A version must first be structurally valid against the reference data and revision graph.

## Next

The next pass should connect validation to RuleSetVersionService.activate so invalid versions cannot be activated.
