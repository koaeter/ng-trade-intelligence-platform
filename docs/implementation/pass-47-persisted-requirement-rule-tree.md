# Pass 47 — Persisted requirement rule tree

## Objective

Create a normalized persistence representation for requirement condition trees without storing executable expressions or opaque evaluator code.

## Implemented

Each requirement rule node stores:
- requirement
- parent node
- sibling sequence
- node type
- group operator when it is a group
- condition field/operator/value when it is a condition

The self-referencing parent relationship preserves arbitrary nesting.

## Security and governance

The database stores declarative rule data, not Python expressions or executable code.

That means a persisted rule cannot become arbitrary code execution simply because a rule is data-driven.

## Next

The next pass should add a builder/loader that turns persisted nodes into the domain ConditionNode tree and validates malformed trees before evaluation.
