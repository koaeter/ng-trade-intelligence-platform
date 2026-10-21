# Pass 144 — Batch-Loaded Requirement Relations

## Goal

Reduce database round trips when scenario evaluation loads the requirement catalogue, without changing which requirements are evaluated or the meaning of their scope.

## Changes

- Replaced per-requirement relation hydration in `SqlAlchemyRequirementRepository.list_all` with batched reads for product, HS-code, origin-country, destination-market, and evidence links.
- Related catalog records are fetched in grouped queries and assembled into immutable domain `Requirement` objects.
- Requirement ordering remains deterministic by ID.
- The single-record `get` path remains unchanged in this pass.
- Added a SQLite-backed unit test that checks scoped requirement hydration and general-scope requirements.

## Semantics and limits

This pass does not yet add a candidate index and does not filter the requirement set. Every requirement is still returned, including inactive and out-of-scope requirements, so the evaluation layer can preserve complete result and trace coverage.

The implementation reduces the former per-requirement relationship/catalog lookups to a bounded set of bulk queries for the full list. Very large catalogues may eventually need chunking to stay within database parameter limits; that should be introduced with explicit tests and without silently dropping requirements.

## Verification

The targeted unit test has been added. CI must complete before this pass is considered verified. Repository-wide Ruff baseline failures have previously been observed and should be distinguished from test failures introduced by this pass.
