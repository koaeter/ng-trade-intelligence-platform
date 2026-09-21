# Pass 24 — Source, Document & Provision Persistence

## Objective

Make the source-first provenance model executable and reconcile the earlier governed master-data changes with the API and PostgreSQL persistence boundary.

## Implemented

### Provenance persistence

Added PostgreSQL persistence for:

- Source
- Document
- Provision
- Evidence provenance references

The provenance chain is now representable as:

```
Source
  ↓
Document
  ↓
Provision
  ↓
Evidence
  ↓
Requirement
```

Evidence may reference a source directly and may additionally reference a document and provision. This allows dataset/source-level evidence without forcing every evidence record to be a provision citation.

### Migration

Added `0004_source_document_provenance.py`.

The migration chain remains:

```
0001_initial_persistence
        ↓
0002_requirement_scope_and_evidence
        ↓
0003_master_data_normalization
        ↓
0004_source_document_provenance
```

The existing `0002` master-data tables are retained as the historical migration boundary; `0003` adds normalized requirement scope and scenario foreign keys rather than recreating those tables.

### Persistence reconciliation

The SQLAlchemy repository layer now:

- imports and implements all governed catalog repository ports;
- resolves Product, HS Code, Country and Market into domain objects;
- persists scenarios using governed identifiers;
- persists Requirement scope through normalized join tables;
- resolves persisted Requirement scope back into domain objects;
- persists Evidence document/provision references;
- implements Source, Document and Provision repositories.

The application/domain boundary therefore remains:

```
API identifiers
   ↓
Application resolution
   ↓
Governed domain objects
   ↓
Repository persistence
```

### API

Added:

- `POST /api/v1/sources`
- `GET /api/v1/sources/{id}`
- `POST /api/v1/documents`
- `GET /api/v1/documents/{id}`
- `POST /api/v1/provisions`
- `GET /api/v1/provisions/{id}`
- `GET /api/v1/evidence/{id}`

Scenario creation now requires an explicit HS version and resolves all product/classification/geographic references through repository ports before creating the domain scenario.

## Deliberate boundary

This pass does **not** ingest real Nigerian legislation or external regulatory sources.

No development fixture is treated as authoritative law.

The next source-oriented step can introduce a controlled fixture and then build the acquisition/ingestion workflow around the same provenance model.

## Tests

Existing unit/API/integration coverage was aligned with the governed Product, HSCode, Country and Market domain objects.

CI status should be checked against the resulting commit before treating the implementation as verified.
