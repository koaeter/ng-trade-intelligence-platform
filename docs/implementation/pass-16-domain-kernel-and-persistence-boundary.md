# Pass 16 — Domain Kernel & Persistence Boundary

## Purpose

Pass 16 introduces the first executable domain concepts and establishes the boundary between deterministic domain logic and future persistence.

## Domain kernel introduced

The first implemented concepts are:

- ExportScenario
- Requirement
- ApplicabilityEvaluation
- EvaluationResult

The scenario contains the minimum context needed for the first deterministic evaluation:

- product
- HS code
- origin
- destination
- scenario date.

## Deterministic evaluation

The first rule implemented is temporal validity.

A requirement is applicable for this initial slice when its effective period contains the scenario date.

This is deliberately simple. It proves the architectural path without pretending that real Nigerian export requirements have already been modelled.

The current evaluation path is:

```text
ExportScenario
      ↓
Requirement
      ↓
Temporal Rule
      ↓
ApplicabilityEvaluation
```

## Important limitation

This is **not yet a real regulatory applicability engine**.

The first rule only proves that:

- domain logic is deterministic
- the application layer can orchestrate the domain
- results have an explicit state
- tests can validate the behaviour.

Product scope, HS scope, destination scope, exceptions, evidence and conflicts will be added incrementally.

## Persistence boundary

The domain objects are intentionally implemented without database dependencies.

The next persistence step will map them into PostgreSQL through repository interfaces and migrations.

Target direction:

```text
Application
    ↓
Repository Interface
    ↓
PostgreSQL Repository
    ↓
PostgreSQL
```

The domain must not import SQLAlchemy, psycopg or PostgreSQL-specific code.

## Testing

Added deterministic tests for:

- requirement effective-period evaluation
- scenario evaluation
- applicability result state.

These tests do not require PostgreSQL or an LLM.

## Next Pass

**Pass 17 — PostgreSQL Persistence & Migration Boundary**

The next pass should implement:

- SQLAlchemy persistence models
- Alembic migrations
- database configuration
- repository interfaces
- PostgreSQL repositories
- application service persistence
- integration tests against PostgreSQL
- scenario create/retrieve flow.

The API can then expose the first real persisted export-scenario resource.
