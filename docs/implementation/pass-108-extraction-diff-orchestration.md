# Pass 108 — Persisted Extraction-Diff Orchestration

Pass 108 connects the Pass 107 segment-level diff domain/service to the persisted extraction lineage.

## What it adds

`GenerateExtractionDiff` is the application orchestration boundary for an existing `ExtractionComparison`.

It:
1. loads the persisted comparison;
2. loads baseline and candidate segments by their immutable extraction-run IDs;
3. delegates diff classification to `CompareExtractionSegments`;
4. persists the immutable `ExtractionDiff`;
5. persists its ordered `ExtractionDiffEntry` records.

The orchestration does not create or modify extraction runs, segments, document versions, or comparisons.

## Governance boundary

The service exposes processing differences only. It does not interpret a diff as a legal amendment, supersession relationship, changed regulatory provision, or changed compliance requirement.

## Transaction boundary

Repositories are responsible for their existing persistence behavior. The orchestration performs the diff and persistence in one application operation, while the caller controls the surrounding database transaction/commit.

## Resulting lineage

**Source → Document → DocumentVersion → SourceArtifact → ExtractionRun → ExtractionComparison → ExtractionDiff → ExtractionDiffEntry**

Pass 108 makes the segment-diff layer executable against persisted extraction lineage without collapsing processing evidence into legal meaning.