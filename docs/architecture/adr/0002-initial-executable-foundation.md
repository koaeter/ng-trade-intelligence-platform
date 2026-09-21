# ADR 0002 — Initial Executable Foundation

## Status

Accepted for initial implementation.

## Context

The platform has completed its conceptual architecture and now needs a minimal executable foundation. The first implementation must prove that the repository can host an API, automated tests, development infrastructure and CI without prematurely implementing the full trade-intelligence domain.

## Decision

Establish:

- Python 3.11+ backend foundation
- FastAPI API entry point
- pytest test framework
- Ruff linting
- mypy type checking
- PostgreSQL development service through Docker Compose
- GitHub Actions CI
- explicit domain/application/contracts package boundaries.

The PostgreSQL service is infrastructure only at this stage. Database persistence and migrations will be added in subsequent implementation stages.

## Consequences

Positive:

- the repository is executable
- local development has a reproducible database service
- CI can validate the backend foundation
- architectural boundaries exist before domain implementation
- infrastructure is not mixed into the API.

Trade-offs:

- the web frontend is not yet implemented
- database migrations are not yet implemented
- the first API is intentionally minimal
- some architecture remains documentation until the vertical slice begins.

## Next step

Implement the initial domain kernel and persistence/migration boundary, then expose the first real export-scenario use case through the API.
