# Pass 128 — Document Provenance Read Model

## Scope

Compose existing document-version and artifact queries into a read-only provenance view.

## Shape

- ordered document versions
- artifacts grouped by their explicit `document_version_id`

## Boundary

This is a read model only. It does not create relationships, select a legally effective version, or infer supersession, amendment, or repeal.