# Pass 18 — Persisted Requirements & Deterministic Evaluation Flow

## Purpose

Pass 18 connects persisted regulatory requirements to the deterministic scenario evaluation service and persists the resulting evaluation records.

## Implemented

Repository ports and PostgreSQL implementations now cover ExportScenario, Requirement, and ApplicabilityEvaluation.

The evaluation flow is:

Persisted ExportScenario -> Persisted Requirements -> Deterministic Temporal Rule -> ApplicabilityEvaluation -> Persisted Evaluation Result

## Evaluation semantics

The current rule remains intentionally narrow: a requirement effective on the scenario date is APPLICABLE; otherwise it is NOT_APPLICABLE. The rule-set version is recorded as initial.

This is still a foundation slice, not the final regulatory applicability engine. Product scope, HS scope, jurisdiction, conditions, exceptions, evidence, conflicts, amendments and source provenance remain future work.

## API

POST /api/v1/export-scenarios/{id}/evaluate
GET /api/v1/export-scenarios/{id}/results

Evaluation is explicit. Creating a scenario does not automatically evaluate it.

## Architectural significance

The system now separates domain rule, application orchestration, and persistence. This is the first executable form of the previously defined deterministic evaluation path.

## Next Pass

Pass 19 — Requirement Scope & Evidence Boundary.
