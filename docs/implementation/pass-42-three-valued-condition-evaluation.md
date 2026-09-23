# Pass 42 — Three-valued requirement condition evaluation

## Objective

Introduce deterministic evaluation of structured requirement conditions without collapsing missing information into false or true.

## Implemented

The evaluator supports:
- TRUE
- FALSE
- UNKNOWN

It evaluates the controlled condition operators introduced in Pass 41 and produces an individual trace for each condition.

For a conjunctive condition set:
- any FALSE makes the set FALSE
- otherwise any UNKNOWN makes the set UNKNOWN
- otherwise the set is TRUE

## Why UNKNOWN matters

If a rule depends on processing history and that fact is missing, the engine must not assume the exporter failed the rule and must not assume the exporter satisfied it.

The result remains UNKNOWN until the required fact is supplied.

## Boundary

This pass evaluates atomic condition candidates. It does not yet implement nested AND/OR rule trees, exceptions, precedence or temporal applicability.

## Next

The next pass should introduce the full rule-condition tree with explicit AND/OR/NOT groups and preserve a machine-readable evaluation trace.
