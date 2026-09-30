# Pass 103 — Document Version and Artifact Lineage

## Objective

Separate publication identity from publication state and exact acquired bytes.

The lineage is now:

Source → Document → DocumentVersion → SourceArtifact → Extraction.

## Implemented

- Added immutable DocumentVersion domain entity.
- Added application repository boundary and registration service.
- Registration requires an existing parent document and rejects duplicate IDs.
- Effective-date intervals are structurally validated.
- Added PostgreSQL persistence for document versions.
- Added an optional document_version_id on source artifacts so existing artifacts remain backward-compatible during migration.
- Added a compound lookup index for document/version temporal queries.

## Semantics

Document identifies the publication as a logical work.

DocumentVersion identifies a particular edition/state of that publication.

SourceArtifact identifies the exact retrieved bytes and remains independently checksum-addressable.

A version is not inferred from a filename, URL, acquisition date, or checksum. A version must be explicitly registered and linked.

The optional artifact link is intentional: existing historical artifacts can be migrated and reviewed without inventing a version assignment.

## Non-goals

This pass does not infer supersession, amendment, replacement, correction, or consolidation relationships.

It does not make a registered document or version authoritative.

It does not automatically assign existing artifacts to versions.

Those controls are addressed by subsequent lineage/governance passes.
