# Pass 118 — Source Artifact API Read Surface

## Goal

Expose the acquired source artifact that anchors extraction provenance.

## Endpoint

GET /api/v1/source-artifacts/{artifact_id}

The response includes source/document lineage, artifact kind, storage key, checksum, acquisition timestamp, processing state, and optional acquisition/document-version references.

## Governance boundary

The endpoint exposes provenance metadata only. It does not interpret the artifact or its extracted content as a legal instrument or compliance requirement.

## Tests

API coverage verifies successful artifact retrieval and missing-artifact handling.
