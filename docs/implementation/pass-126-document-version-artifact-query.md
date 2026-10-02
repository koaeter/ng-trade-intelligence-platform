# Pass 126 — Document Version Artifact Query

## Scope

Add an application read boundary for artifacts explicitly attached to a document version.

## Semantics

The query preserves artifact provenance and does not infer legal status from artifact presence, checksums, extraction results, or version dates.

## Infrastructure follow-up

The existing SQLAlchemy artifact repository will need the corresponding version-scoped list implementation before this query is exposed through the API.