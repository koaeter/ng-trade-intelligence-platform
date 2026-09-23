# Pass 44 — Temporal validity evaluation

## Objective

Make scenario-date evaluation explicit and reproducible instead of selecting rules merely because they are present in the current database.

## Implemented

TemporalValidity distinguishes:
- effective_from
- effective_to
- scenario date

The end date is treated as exclusive:

effective_from <= scenario_date < effective_to

An open-ended effective_to remains active after effective_from.

## Why this matters

A regulation can be published before it becomes effective, and an older rule can remain historically relevant after it has been superseded.

Historical evaluation must use the rule state applicable to the scenario date.

## Next

The next pass should combine temporal validity with requirement scope and condition evaluation into a single deterministic applicability decision.
