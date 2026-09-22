# Pass 25 — Controlled Regulatory Fixture & Knowledge Ingestion Boundary

## Objective

Move the platform from persisted source/provision records to a controlled development
knowledge path while keeping authoritative publication evidence-first.

## What changed

- Added source lifecycle states: DISCOVERED, ACQUIRED, EXTRACTED, CANDIDATE,
  REVIEWED, PUBLISHED, SUPERSEDED, RETIRED.
- Added sources.status through migration 0005_source_lifecycle.
- Added a small application ingestion boundary in packages/application/ingestion/services.py.
- Publication requires a reviewed source, valid document/provision relationships,
  verified evidence, and an explicit evidence reference from the requirement.
- Added scripts/seed_regulatory_fixture.py.

## Development fixture

The fixture is intentionally fictional and non-authoritative:

~~~text
development-regulatory-fixture
        ↓
development-export-guideline
        ↓
DEV-4.2
        ↓
evidence-dev-001
        ↓
dev-export-document-requirement
~~~

It is only for exercising persistence, provenance, and deterministic applicability.
It must not be presented as Nigerian law or official guidance.

Run after the master-data seed:

~~~text
python scripts/seed_master_data.py
python scripts/seed_regulatory_fixture.py
~~~

## Publication boundary

The ingestion service deliberately does not call an LLM or permit AI to publish
knowledge. AI/extraction may eventually create candidates, but a reviewed source and
verified evidence are required before publication.

## Migration chain verification

The current migration chain is:

~~~text
0001_initial_persistence
        ↓
0002_requirement_scope_and_evidence
        ↓
0003_master_data_normalization
        ↓
0004_source_document_provenance
        ↓
0005_source_lifecycle
~~~

A reconciliation review confirmed that the master-data tables are created in 0002,
while 0003 normalizes scenario and requirement relationships rather than recreating
those tables.

## Verification note

Repository code was reconciled against the migration chain during this pass.
CI status must be checked separately before claiming a passing build.
