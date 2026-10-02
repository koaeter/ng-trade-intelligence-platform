# Pass 119 — Artifact Extraction Run API

## Goal

Expose the extraction runs associated with a source artifact so provenance can be traversed from the acquired artifact into each immutable processing execution.

## Endpoint

GET /api/v1/source-artifacts/{artifact_id}/extraction-runs

The endpoint delegates to the application query contract and returns extraction-run metadata without mutating state.

## Governance boundary

The relationship between an artifact and its extraction runs is processing provenance. It does not establish legal effect or compliance significance.

## Tests

Coverage verifies artifact-scoped extraction-run listing.
