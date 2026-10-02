# Pass 107 — Segment-Level Document/Extraction Diffing

Pass 107 adds an immutable, auditable diff between two extraction runs.

## What it detects

Each diff entry is one of:

- `UNCHANGED` — the segment text matched exactly.
- `ADDED` — a candidate segment has no matching baseline segment.
- `REMOVED` — a baseline segment has no matching candidate segment.
- `MODIFIED` — corresponding segments occupy a replacement block and their text differs.

Matching is sequence-aware but does not rely on sequence numbers alone. An inserted segment therefore does not automatically make every later segment appear modified.

## Provenance retained

Every entry retains, where available, both sides':

- extraction segment ID
- sequence
- SHA-256 of segment text
- page number
- section
- source start/end offsets
- locator

This keeps the diff useful for later review without rewriting either extraction run.

## Persistence

Pass 107 adds:

- `extraction_diffs`
- `extraction_diff_entries`
- immutable diff repository contracts and SQLAlchemy repositories
- migration `0036_extraction_diffs`

A diff is linked to the Pass 106 `ExtractionComparison`. The comparison remains the processing-level change record; the diff supplies segment-level detail.

## Determinism and bounds

Segments are ordered by `(sequence, id)`. Python's deterministic `SequenceMatcher` with `autojunk=False` is used over segment text. The service defaults to a maximum of 10,000 segments per side to keep the comparison bounded.

Diff entry IDs use the immutable diff ID plus ordinal, making their identity stable within the diff.

## Governance boundary

The diff describes extraction/output differences only. It does not infer:

- that a legal instrument was amended;
- that a document version supersedes another;
- that a provision is legally changed;
- that a regulatory requirement changed.

Those conclusions require separately verified document relationships and governed review.

## Resulting lineage

**Source → Document → DocumentVersion → SourceArtifact → ExtractionRun → ExtractionComparison → ExtractionDiff → ExtractionDiffEntry**

The original extraction runs and segments remain unchanged.
