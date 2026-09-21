# ADR 0003 — PostgreSQL Persistence Boundary

## Status

Accepted

## Decision

Use PostgreSQL as the initial authoritative application/domain persistence store, accessed through SQLAlchemy repositories and Alembic migrations.

The domain model remains persistence-ignorant. Database schemas and ORM models live in infrastructure.

## Rationale

- domain logic remains deterministic and testable
- PostgreSQL supports the relational source-of-truth model
- migrations provide explicit schema history
- repository ports keep application orchestration independent of database implementation

## Consequences

- real persistence is available for the first vertical slice
- integration tests can exercise PostgreSQL
- schema changes are versioned
- later projections can consume governed relational data
- repository mapping adds code
- integration testing requires a database service

## Rejected shortcut

The application does not call Base.metadata.create_all() during normal startup. Production schema evolution is migration-driven.
