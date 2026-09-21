# Development Getting Started

## Current status

Pass 15 establishes the first executable backend foundation. The platform is still in development and does not yet contain authoritative trade-regulatory data.

## Prerequisites

- Python 3.11+
- Docker
- Git

## Backend

Create a virtual environment and install development dependencies:

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -e ".[dev]"
```

Start the API:

```bash
uvicorn apps.api.main:app --reload
```

Health endpoint: `GET /health`

## PostgreSQL

```bash
docker compose up -d postgres
```

The database is currently development infrastructure only. Application persistence will be introduced in a later pass.

## Tests

```bash
pytest
```

## Linting

```bash
ruff check .
```

## Type checking

```bash
mypy apps packages infrastructure
```

## Architecture rule

The current foundation deliberately keeps the API small. Domain and application packages are architectural boundaries, not invitations to create speculative abstractions before the first vertical slice.
