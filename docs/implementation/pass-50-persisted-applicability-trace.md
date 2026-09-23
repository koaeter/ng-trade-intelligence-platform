# Pass 50 — Persisted applicability trace

## Objective

Create a durable audit boundary for deterministic requirement evaluations.

## Implemented

Applicability traces now have a persistence contract containing:
- scenario
- requirement
- scenario date
- rule-set version
- temporal result
- scope result
- condition result
- evidence result
- final result

The trace is separate from the user-facing evaluation record so audit history can be retained without overloading the existing result model.

## Reproducibility principle

A historical evaluation must identify the rule-set version used to produce it. The scenario date remains the legal evaluation date; the evaluation timestamp and retrieval dates are separate concerns.

## Next

The next pass should implement the SQLAlchemy trace repository and connect deterministic evaluation persistence to it.
