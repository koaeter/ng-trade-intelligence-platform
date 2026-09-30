# Pass 104 — Document Version Relationships

## Objective

Create an explicit governance layer for relationships between document versions.

## Implemented

- Added controlled relationship types:
  - SUPERSEDES
  - AMENDS
  - REPLACES
  - CORRIGES
  - CONSOLIDATES
  - ANNEX_OF
  - DERIVED_FROM
- Added immutable relationship domain entity.
- Added application repository boundary.
- Added registration service requiring both referenced versions to exist.
- Self-referential relationships are rejected.
- Verified relationships require an evidence reference.
- Added PostgreSQL persistence and indexes.

## Governance semantics

Relationships are explicit records. The system does not infer them from filenames, publication dates, URLs, checksums, or acquisition order.

An unverified relationship may be recorded as a candidate relationship, but it must not be treated as verified lineage.

This pass does not determine legal effect or automatically change document lifecycle status.

## Non-goals

No automatic supersession inference.

No automatic retirement of a prior document.

No legal conclusion from relationship type alone.

No automatic propagation of requirements between versions.
