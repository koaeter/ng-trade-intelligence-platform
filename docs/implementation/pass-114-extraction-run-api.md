# Pass 114 — Extraction Run API Read Surface

## Goal

Expose immutable extraction-run metadata through the existing FastAPI application.

## Endpoint

GET /api/v1/extraction-runs/{extraction_id}

The endpoint returns the artifact and document-version lineage, input checksum, extractor identity/version, extraction timestamp, and OCR flag. Missing runs return 404.

## Governance boundary

The endpoint exposes processing provenance only. It does not interpret extracted content or determine legal significance.

## Tests

API coverage verifies successful extraction-run retrieval and missing-run handling.
