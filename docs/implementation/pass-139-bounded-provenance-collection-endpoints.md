# Pass 139 — Bounded Provenance Collection Endpoints

## Goal

Close the remaining collection-response bypasses around the provenance model.

Pass 137 bounded the expanded document-provenance endpoint, and Pass 138 moved that bound into SQLAlchemy queries. Pass 139 applies the same bounded-query contract to dedicated collection endpoints.

## Endpoints bounded

The following collection endpoints now accept `limit`, defaulting to 100 and capped at 500:

- document-version relationships
- document versions for a document
- source artifacts for a document version
- extraction runs for an artifact
- extraction segments for an extraction run
- extraction diffs for a comparison

The existing single-record endpoints remain unchanged.

## Layering

The bound is propagated through:

`API Query parameter → application query service → repository contract → SQLAlchemy LIMIT`

This keeps the API policy explicit while ensuring the database does not materialize an unbounded collection for these endpoints.

## Boundary

This pass is a resource-safety and response-shaping change. It does not alter source provenance semantics and does not infer legal effect, supersession, amendment, repeal, applicability, or compliance conclusions.

The dedicated collection endpoints complement the three provenance access levels:

1. summary
2. bounded expanded provenance
3. bounded/dedicated detail collection retrieval

