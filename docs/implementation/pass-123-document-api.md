# Pass 123 — Document API Read Surface

## Goal

Expose the immutable document identity above document versions and extraction provenance.

## Endpoint

GET /api/v1/documents/{document_id}

The response contains source linkage, title, document type, publication/effective dates, and version label.

## Governance boundary

Document metadata is exposed as recorded. The API does not infer whether a document is legally operative, superseded, repealed, or applicable to an export scenario.

## Tests

Coverage verifies document retrieval and missing-document handling.
