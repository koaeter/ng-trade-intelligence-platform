# Pass 142 — Bounded Authority Endpoint Collections and API Surface Cleanup

## Goal

Close the remaining unbounded authority-endpoint collection identified during the resource-safety audit and remove a duplicate document route declaration.

## Changes

- Added an optional database-level `limit` to `SqlAlchemyAuthorityEndpointRepository.list_for_authority`.
- Preserved deterministic ordering by endpoint type and URL before applying the limit.
- Added `limit=100` as the API default and `limit<=500` validation to:
  `GET /api/v1/authorities/{authority_id}/endpoints`.
- Added API regression coverage proving the requested limit reaches the repository and that values above 500 are rejected.
- Corrected the API import to use the dedicated authority-endpoint repository module.
- Removed the later duplicate `GET /api/v1/documents/{document_id}` declaration so the typed document endpoint is the single route for that resource.

## Architectural effect

This pass does not introduce authentication or authorization. It is strictly a resource-safety and API-surface consistency change.

The bounded-collection convention is now also applied to authority endpoint discovery:

`collection endpoint -> API bound -> repository bound -> deterministic ordering`

The limit is a retrieval bound, not a statement that the authority has only that many endpoints.

## Verification

Targeted tests cover:

1. forwarding a custom collection limit to the repository;
2. rejecting a limit above the API maximum.

Repository-wide CI should still be interpreted separately from these targeted checks because the project has a pre-existing Ruff baseline that is not caused by this pass.
