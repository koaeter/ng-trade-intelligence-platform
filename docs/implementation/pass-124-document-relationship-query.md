# Pass 124 — Document Relationship Query

## Scope

Expose read-only application queries for the explicit relationship graph between document versions.

## Behavior

- `GetDocumentRelationship` retrieves one relationship by ID.
- `ListDocumentRelationships` retrieves relationships touching a document version.
- Missing single relationships raise a `ValueError`.
- Query operations do not mutate relationship or document-version state.

## Boundary

Relationship records describe explicitly registered provenance relationships such as amendment, supersession, replacement, corrigenda, consolidation, annex, or derivation. They do not themselves constitute an automated legal conclusion.

## Next

The API surface can expose these immutable relationship records without introducing a new aggregate.
