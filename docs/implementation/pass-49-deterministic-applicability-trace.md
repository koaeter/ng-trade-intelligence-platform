# Pass 49 — Deterministic applicability trace

## Objective

Combine temporal validity, requirement scope, structured conditions and evidence into one deterministic evaluation boundary.

## Implemented

The service evaluates in order:

1. temporal validity
2. product/HS/origin/destination scope
3. structured condition tree
4. evidence sufficiency and verification
5. final result

The result is represented by an ApplicabilityTrace that records each stage.

## Result semantics

- invalid date -> NOT_APPLICABLE
- explicit scope mismatch -> NOT_APPLICABLE
- missing scope -> UNRESOLVED
- false condition -> NOT_APPLICABLE
- unknown condition -> UNRESOLVED
- missing evidence -> INSUFFICIENT_EVIDENCE
- unverified evidence -> UNRESOLVED
- verified evidence with satisfied rule -> APPLICABLE

## Next

The next pass should persist the evaluation trace and rule-set version so a historical result can be reproduced and audited.
