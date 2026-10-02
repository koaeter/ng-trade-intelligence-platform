# Pass 116 — Extraction Segment API Read Surface

## Goal

Expose the bounded extraction fragments used to audit extraction comparisons and diffs.

## Endpoints

- GET /api/v1/extraction-segments/{segment_id}
- GET /api/v1/extraction-runs/{extraction_id}/segments

The single-segment endpoint returns source-location metadata and extracted text. The run-scoped endpoint returns the segments associated with one extraction run in repository sequence order.

## Governance boundary

The API exposes extracted source evidence only. It does not classify the text as legally operative, amended, repealed, superseded, or compliance-changing.

## Tests

Coverage verifies single-segment retrieval, missing-segment handling, and run-scoped segment listing.
