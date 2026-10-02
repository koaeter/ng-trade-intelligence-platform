# Pass 112 — Extraction Comparison API Read Surface

## Goal

Expose immutable extraction-comparison metadata through the existing FastAPI application, completing the read path immediately above extraction diffs.

## Endpoint

GET /api/v1/extraction-comparisons/{comparison_id}

The endpoint returns:

- baseline and candidate extraction IDs;
- baseline and candidate input checksums;
- baseline and candidate output hashes;
- deterministic comparison result;
- comparison timestamp.

Missing comparisons return 404.

## Lineage

The read path is now:

ExtractionComparison → ExtractionDiff → ExtractionDiffEntry

The API remains a processing-evidence surface. It does not interpret a comparison as an amendment, repeal, supersession, legal change, or compliance requirement change.

## Tests

API coverage verifies successful comparison retrieval and missing-comparison handling.
