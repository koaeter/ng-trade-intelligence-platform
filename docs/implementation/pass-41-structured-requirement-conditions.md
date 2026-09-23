# Pass 41 — Structured requirement conditions

## Objective

Give requirement candidates a controlled representation for conditions that cannot be expressed as simple product, HS, origin, destination or date scope.

## Implemented

Supported condition fields include:
- quantity
- value
- exporter type
- intended use
- processing state
- certificate availability
- agreement status
- preference claimed

Supported operators include:
- equals / not equals
- in / not in
- greater/less comparisons
- exists / does not exist

Conditions are still candidates. No deterministic evaluator consumes them yet.

## Why this boundary matters

A regulatory sentence such as "where the exporter is a manufacturer" must eventually become a structured condition rather than remain an opaque prompt fragment.

The system can now distinguish:

Requirement scope
  +
structured condition
  +
source evidence

before the applicability engine is asked to evaluate anything.

## Next

The next pass should add persistence mapping for condition candidates and a normalized condition-set abstraction suitable for deterministic three-valued evaluation.
