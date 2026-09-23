# Pass 59 — Rule-set activation validation

## Objective

Make RuleSetVersionService enforce the publication validation boundary before changing activation state.

## Implemented

Rule-set activation now:
1. resolves the target
2. validates the target when a validator is configured
3. retires the previous active version
4. activates the validated target

Validation failures therefore prevent activation.

## Next

The next pass should introduce a formal rule-set publication status so versions move through draft, validated, published and retired states rather than jumping directly between active/retired.
