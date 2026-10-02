# Pass 117 — Source Artifact Query Surface

## Goal

Provide an application read contract for immutable acquired source artifacts, the provenance anchor for extraction runs and segments.

## Contract

GetSourceArtifact retrieves one artifact by ID and rejects missing artifacts.

The query exposes acquisition identity and processing state without changing the artifact.

## Provenance chain

SourceArtifact → ExtractionRun → ExtractionSegment → ExtractionComparison → ExtractionDiff → ExtractionDiffEntry

This chain is processing provenance. It does not itself establish legal effect or compliance impact.

## Tests

Coverage verifies successful artifact retrieval and missing-artifact rejection.
