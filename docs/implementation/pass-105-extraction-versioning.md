# Pass 105 — Extraction Versioning

## Purpose

Pass 105 gives each extraction execution an immutable identity.

The lineage is now:

**Source → Document → DocumentVersion → SourceArtifact → ExtractionRun → ExtractionSegment → ProvisionCandidate**

An extraction run records the exact artifact checksum, the document version carried by that artifact, extractor identity/version, extraction time, and OCR usage.

## Rules

1. An extraction run is append-only and independently identified from the artifact.
2. Re-running extraction can create a new run for the same artifact.
3. The artifact checksum is captured on the run, so extractor changes are distinguishable from source-content changes.
4. New extraction segments carry the extraction-run ID.
5. Existing segments are not retroactively assigned to a run because their historical run cannot be established safely.
6. The document-version ID is copied from the artifact as lineage metadata; it is not independently inferred.
7. Extraction remains non-authoritative: it records processing provenance, not regulatory meaning.
8. The legacy artifact-level extracted-text representation remains available for compatibility.

## Result

A newly generated provision candidate can now be traced through its extraction segment to the exact extraction execution and then to the source artifact and document version.

## Next pass

The next layer is **re-extraction and change detection**: compare extraction runs without overwriting historical provenance.
