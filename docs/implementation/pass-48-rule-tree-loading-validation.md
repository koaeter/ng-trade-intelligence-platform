# Pass 48 — Rule-tree loading and validation

## Objective

Turn persisted declarative rule nodes into an executable domain ConditionNode tree only after structural validation.

## Implemented

Validation covers:
- exactly one root
- matching requirement ownership
- valid parent references
- duplicate IDs
- cycles
- unreachable nodes
- valid group operators
- valid condition field/operator pairs
- correct child cardinality for AND, OR and NOT

The database therefore remains a declarative representation while the evaluator receives a validated in-memory structure.

## Next

The next pass should integrate the loaded rule tree into requirement applicability evaluation and preserve the condition-level trace alongside scope, temporal and evidence decisions.
