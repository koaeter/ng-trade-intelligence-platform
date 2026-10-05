# Pass 140 — Bounded Extraction Diff Detail

## Goal

Prevent a single extraction-diff detail request from materializing an arbitrarily large diff-entry collection.

## Contract

`GET /api/v1/extraction-diffs/{diff_id}` now accepts:

- `entry_limit`: default 100, minimum 1, maximum 500

The response retains the existing `entry_count` metadata and adds:

- `entries_truncated: true|false`

When entries are truncated, the response contains the first bounded entries in ordinal order while `entry_count` continues to represent the complete diff count.

## Implementation

The application query requests `entry_limit + 1` entries from the repository. The extra record determines truncation without an unbounded database result.

The repository applies SQL LIMIT at the database layer.

## Architectural boundary

This limits resource usage and response expansion only. It does not alter extraction-diff semantics and does not convert extraction differences into legal conclusions.

