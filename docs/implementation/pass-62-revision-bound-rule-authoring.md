# Pass 62 — Revision-bound rule authoring

## Objective

Ensure persisted requirement condition trees can only be authored for requirement revisions that belong to the target rule-set draft.

## Implemented

The rule authoring service:
- verifies rule-set membership
- verifies logical requirement identity
- verifies immutable revision identity
- flattens a validated domain ConditionNode tree into normalized persistence nodes
- preserves parent/child order
- stores the revision ID on every node

## Governance effect

A condition tree cannot be attached to an unrelated requirement or revision.

## Next

The next pass should add rule-tree editing/replacement semantics so revisions remain immutable while draft rule-set authoring can correct candidate rules safely.
