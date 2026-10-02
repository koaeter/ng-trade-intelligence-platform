# Pass 113 — Extraction Run Query Surface

## Goal

Provide application read contracts for immutable extraction runs, establishing a stable query boundary before API exposure.

## Contracts

- GetExtractionRun retrieves one extraction run by ID and rejects missing runs.
- ListExtractionRunsForArtifact lists extraction runs belonging to one source artifact.

Both operations are read-only and preserve the extraction-run record as immutable processing evidence.

## Governance boundary

An extraction run records how an artifact was processed. It does not establish legal meaning, document supersession, or compliance impact.

## Tests

Coverage verifies successful retrieval, missing-run rejection, and artifact scoping.
