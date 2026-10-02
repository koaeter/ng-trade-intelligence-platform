# Pass 120 — Extracted Text Query and API

## Goal

Expose the immutable extracted-text record associated with a source artifact.

## Contract

GetExtractedText retrieves extracted text by artifact ID and rejects missing records.

## Endpoint

GET /api/v1/source-artifacts/{artifact_id}/extracted-text

The response includes extracted text, extractor identity/version, extraction timestamp, and OCR usage.

## Governance boundary

Extracted text is processing output. This surface does not decide whether text is legally operative or whether it changes an export-compliance obligation. Segment-level and downstream governed interpretation remain separate.

## Tests

Coverage verifies successful retrieval and missing extracted-text handling.
