# Pass 46 — Deterministic applicability scope hardening

## Objective

Close the ambiguity between an explicitly general requirement and a requirement whose applicability scope has not been established.

## Implemented

The applicability service now distinguishes:
- explicit scoped requirements
- explicitly general requirements
- requirements with no established scope

An empty scope is no longer enough by itself to imply universal applicability. A requirement must carry the explicit general-scope flag introduced in Pass 45.

## Evaluation behavior

Temporal invalidity -> NOT_APPLICABLE
Explicit scope mismatch -> NOT_APPLICABLE
Missing scope with no general confirmation -> UNRESOLVED
General scope + missing evidence -> INSUFFICIENT_EVIDENCE
General/scoped scope + verified evidence -> APPLICABLE

## Why this matters

The platform should never turn an absence of structured scope into an assumption that a legal requirement applies everywhere.

## Next

The next pass should attach structured condition rule trees to requirements and combine scope, time, conditions and evidence into one traceable applicability evaluation.
