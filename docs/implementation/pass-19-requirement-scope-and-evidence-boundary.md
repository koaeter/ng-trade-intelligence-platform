# Pass 19 — Requirement Scope & Evidence Boundary

## Goal

Move the executable applicability slice beyond temporal validity by introducing structured requirement scope and a minimal evidence/provenance boundary.

## Implemented

Requirements now support optional scope sets for product IDs, HS codes, origin countries, destination markets, plus evidence identifiers.

The evaluator now distinguishes:

- `NOT_APPLICABLE` when a current requirement has a constrained scope that does not match the scenario.
- `INSUFFICIENT_EVIDENCE` when an effective matching requirement has no evidence.
- `UNRESOLVED` when supplied evidence exists but is not verified.
- `APPLICABLE` when an effective requirement has matching scope and verified evidence.

## Evidence model

A minimal Evidence value object is now present with:

- evidence ID
- evidence type
- source ID
- locator
- excerpt
- verification state

Evidence remains deliberately separate from the full source/document/provision graph. The next source-ingestion passes will connect these concepts to authoritative material.

## Persistence

PostgreSQL models and an Alembic migration now persist requirement scope, evidence, and requirement identity on applicability evaluations.

## Important limitation

This is not yet a legal applicability engine. Scope is currently represented by governed identifier sets, and evidence is a minimal traceability object. No claim of legal authority is inferred merely from an evidence record.

## Architectural milestone

The evaluation path is now conservative and traceable:

`Scenario + Requirement Scope + Effective Date + Evidence -> Evaluation State`

The domain remains independent of SQLAlchemy and PostgreSQL.

## Next

Pass 20 will make Product, HS Code, Country, and Market first-class domain concepts and replace raw scenario strings with governed references.
