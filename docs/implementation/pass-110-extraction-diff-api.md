# Pass 110 — Extraction Diff API Read Surface

## Goal

Expose the immutable extraction-diff query surface through the existing FastAPI application without introducing legal interpretation into the API layer.

## Endpoints

- GET /api/v1/extraction-diffs/{diff_id}
  - Returns the diff summary and its entries ordered by ordinal.
  - Returns 404 when the diff does not exist.

- GET /api/v1/extraction-comparisons/{comparison_id}/diffs
  - Returns diff summaries scoped to an existing extraction comparison.
  - Returns 404 when the comparison does not exist.

## Governance boundary

The API exposes extraction evidence and lineage only:

ExtractionComparison → ExtractionDiff → ExtractionDiffEntry

The response does not infer whether a textual difference represents an amendment, repeal, supersession, legal change, or compliance requirement change. Those interpretations remain downstream governed processes.

## Immutability

Both endpoints are read-only. They do not mutate extraction runs, segments, comparisons, diffs, or entries.

## Tests

The API tests cover:

- complete diff retrieval with ordered entries;
- missing diff handling;
- comparison-scoped listing;
- missing comparison handling.
