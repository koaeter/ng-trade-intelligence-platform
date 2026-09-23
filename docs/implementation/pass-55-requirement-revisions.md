# Pass 55 — Immutable requirement revisions

## Objective

Create a snapshot boundary so historical rule-set evaluation does not depend on mutable current Requirement records.

## Implemented

A RequirementRevision captures:
- logical requirement ID
- revision identifier
- name
- effective period
- product scope IDs
- HS version/code scope
- origin and destination scope
- evidence references
- explicit general-scope state

The revision is a value snapshot, not a live ORM relationship.

## Historical evaluation direction

RuleSet
  -> RequirementRevision
  -> Rule nodes / conditions
  -> evaluation

This separates current editorial state from historical evaluation state.

## Next

The next pass should bind persisted rule nodes to a requirement revision and validate that a rule-set membership references an existing immutable revision.
