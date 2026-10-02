# Pass 122 — Document Version API Read Surface

## Goal

Expose immutable document-version identity above the extraction provenance chain.

## Endpoints

- GET /api/v1/document-versions/{version_id}
- GET /api/v1/documents/{document_id}/versions

The response preserves publication/effective dates and revision references without assigning legal supersession meaning.

## Governance boundary

Version identity and dates are factual metadata. Whether one version supersedes another remains a governed domain process and is not inferred by this API.

## Tests

Coverage verifies single-version retrieval and document-scoped version listing.
