# Pass 121 — Document Version Query Surface

## Goal

Expose a stable application read contract for immutable document versions that anchor extraction runs to a particular publication state.

## Contracts

- GetDocumentVersion retrieves one version by ID.
- ListDocumentVersions lists versions belonging to one document.

## Provenance relationship

DocumentVersion provides the publication-state identity above SourceArtifact and ExtractionRun. The query layer does not decide whether one version legally supersedes another.

## Tests

Coverage verifies direct retrieval, missing-version rejection, and document scoping.
