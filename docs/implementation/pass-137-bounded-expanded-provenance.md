# Pass 137 — Bounded Expanded Provenance

## Goal

Keep the expanded document provenance endpoint useful for navigation without allowing an unbounded response to grow with every provenance collection.

## API contract

The expanded endpoint now accepts:

- `limit`: maximum number of records returned from each provenance collection.
- Default: `100`.
- Minimum: `1`.
- Maximum: `500`.

Example:

`GET /api/v1/documents/{document_id}/provenance?limit=25`

The response includes `truncated_collections`, identifying collections that contained more records than the requested limit.

## Three-level provenance access

1. **Summary** — `/provenance/summary` provides count-only navigation metadata.
2. **Expanded** — `/provenance?limit=N` provides bounded graph expansion.
3. **Detail** — existing collection-specific endpoints remain the path for exhaustive retrieval.

This avoids forcing clients to choose between an unusably large graph and losing provenance navigation entirely.

## Boundary

The bound is a response-expansion safeguard. It does not infer legal meaning from relationships, extraction differences, or truncation state. The underlying provenance records remain authoritative and are retrievable through the dedicated detail APIs.

## Implementation

The application query applies the same explicit limit to every expanded collection and records which collections were truncated. Descendant expansion proceeds only from the records included within the bound, preventing the response graph from expanding through omitted parent records.

The summary endpoint remains independent of the expanded limit.
