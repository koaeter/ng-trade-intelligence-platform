# Pass 127 — Document Version Artifact API

## Scope

Expose source artifacts explicitly attached to a document version.

## Endpoint

- `GET /api/v1/document-versions/{version_id}/artifacts`

## Semantics

The endpoint is provenance-only. It returns artifacts linked by `document_version_id`, ordered by acquisition timestamp and artifact ID. It does not infer document validity, legal effect, supersession, or compliance impact.

Missing document versions return HTTP 404.