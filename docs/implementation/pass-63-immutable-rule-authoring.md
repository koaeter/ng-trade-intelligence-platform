# Pass 63 — Immutable rule authoring

## Objective

Prevent draft rule-set editing from mutating a requirement revision that may already belong to another rule set.

## Decision

Rule trees are part of the immutable requirement revision.

If a rule must change:
- create a new requirement revision
- author the new rule tree against that revision
- include the new revision in a future rule-set version

The existing revision and its rule tree remain unchanged.

## Why

A single requirement revision may be reused by multiple rule-set versions. Editing its rule tree in place would silently alter historical evaluations.

## Implemented

- Rule authoring checks whether a revision already has a tree.
- Existing revisions cannot be edited in place.
- Repository boundary now exposes revision-level lookup.

## Next

The next pass should strengthen requirement revision creation so revision identifiers are immutable and revisions can be compared/diffed before publication.
