# Pass 115 — Extraction Segment Query Surface

## Goal

Provide application read contracts for immutable extraction segments, the bounded source fragments used by extraction comparisons and diffs.

## Contracts

- GetExtractionSegment retrieves one segment by ID.
- ListExtractionSegments lists segments belonging to one extraction run.

The repository interface now includes direct segment lookup rather than requiring a fabricated artifact scope.

## Governance boundary

Segments are extraction evidence. The query layer does not infer legal effect, amendment, repeal, supersession, or compliance impact from segment content.

## Tests

Coverage verifies direct lookup, missing-segment rejection, and extraction scoping.
