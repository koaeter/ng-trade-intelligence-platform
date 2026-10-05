# Pass 141 — Bounded Source Acquisition History

## Goal

Bound source acquisition history because acquisition events are append-only operational provenance and can grow without a natural response-size ceiling.

## Contract

`GET /api/v1/sources/{source_id}/acquisition-events` now accepts `limit`, defaulting to 100 and capped at 500.

The limit flows through the application service and repository to the SQLAlchemy query.

## Ordering

Existing newest-first ordering is preserved:

`started_at DESC, id DESC`

The database limit is applied after that deterministic ordering, so the endpoint returns the newest bounded slice.

## Boundary

This is an operational resource-safety change. It does not change acquisition records, artifact provenance, source authority, or legal interpretation.

