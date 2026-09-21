# Pass 17 — PostgreSQL Persistence & Migration Boundary

## Purpose

Pass 17 turns the domain kernel into a persistable application slice without moving database concerns into the domain layer.

## Implemented

- SQLAlchemy 2.x persistence models
- psycopg PostgreSQL driver
- Alembic migration tooling
- environment-based database configuration
- SQLAlchemy session factory
- PostgreSQL repository implementation
- persisted ExportScenario, Requirement, and ApplicabilityEvaluation tables

## Boundary

API -> Application Service -> Repository Interface -> SQLAlchemy Repository -> PostgreSQL

The domain remains free of SQLAlchemy, psycopg, PostgreSQL, and ORM annotations.

## Scenario resource

The API now exposes:

POST /api/v1/export-scenarios
GET /api/v1/export-scenarios/{id}

The create operation constructs a domain ExportScenario, persists it through the repository port, commits the transaction, and returns the resource representation.

## Migration boundary

Local PostgreSQL is provided by Docker Compose. CI starts PostgreSQL as a service and supplies TEST_DATABASE_URL for integration tests.

Migration command: alembic upgrade head

Schema evolution is migration-driven rather than performed automatically during application startup.

## Testing

Added repository/application boundary tests, a PostgreSQL repository round-trip integration test, and API contract validation tests.

The PostgreSQL integration test is skipped when TEST_DATABASE_URL is absent; CI provides the service and variable.

## Deliberate limits

This pass does not yet implement full Product/HS/Country/Market persistence, persisted evidence and provenance, real regulatory source data, complete applicability evaluation, authentication/authorization, or GraphRAG/vector retrieval.

## Next Pass

Pass 18 — Persisted Requirements & Deterministic Evaluation Flow.
