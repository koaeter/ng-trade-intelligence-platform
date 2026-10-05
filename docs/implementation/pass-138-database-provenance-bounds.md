# Pass 138 — Database-Level Provenance Bounds

## Goal

Move the expanded document-provenance safety bound into the repository query layer so bounded API requests also bound database result materialization.

## Implementation

The provenance list repository contracts now accept an optional `limit` parameter. SQLAlchemy implementations apply the limit after their deterministic ordering.

The expanded provenance application service requests `limit + 1` records for each collection. The extra record preserves the existing ability to detect truncation while still preventing unbounded result materialization.

Bounded collections include:

- document versions
- source artifacts
- document relationships
- extraction runs
- extraction segments
- extraction comparisons
- extraction diffs
- extraction diff entries

The API continues to expose a maximum request limit of 500.

## Behavioral contract

- No limit supplied to ordinary repository callers preserves the existing unbounded repository behavior through SQLAlchemy's `limit(None)` semantics.
- Expanded provenance requests remain bounded at the API boundary.
- The provenance service records a collection in `truncated_collections` when the `limit + 1` query returns more than the requested response limit.
- Descendant expansion only follows records included in the bounded parent collection.
- Ordering remains deterministic before applying the SQL limit.

## Architectural boundary

This is a response-expansion and database-work safeguard only. It does not infer legal effect, supersession, amendment, repeal, applicability, or compliance conclusions from provenance or extraction data.

The provenance hierarchy remains:

`Document → DocumentVersion → SourceArtifact → ExtractionRun → ExtractionSegment → ExtractionComparison → ExtractionDiff → ExtractionDiffEntry`

Summary mode, bounded expanded mode, and dedicated detail endpoints remain the three access levels.

## Verification

Application and API tests were updated so repository fakes accept the new optional limit contract. CI is the authoritative execution environment for the repository test suite.
