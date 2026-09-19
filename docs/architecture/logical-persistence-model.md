# Logical Persistence Model & Storage Boundary

## 1. Purpose

This document defines where the platform's information should logically live. It does not yet select specific technologies.

The objective is to establish authoritative storage responsibilities, relational application data, knowledge graph projections, document/object storage, trade-data analytical storage, search indexes, cache/read models, keys and relationships, temporal storage, provenance storage, transaction boundaries, and synchronization rules.

Technology selection should follow this model rather than drive it.

## 2. Storage Principles

### 2.1 One Authoritative Owner Per Data Class

The same information may be projected into multiple stores, but one store should be considered authoritative for each data class.

Example:

    Regulatory document
        ↓
    Document/Object Store = authoritative artifact
        ↓
    Text extraction / metadata
        ↓
    Relational + Search + Graph projections

### 2.2 Projections Are Rebuildable

Search indexes, graph projections and caches should be considered derived representations wherever practical. If a projection is lost, the platform should be able to reconstruct it from authoritative data.

### 2.3 Store Data According to Access Pattern

Different workloads have different storage characteristics:

- transactional application state
- relationship-heavy knowledge
- full-text retrieval
- large documents
- analytical trade data.

One storage technology does not need to perform every role.

## 3. Logical Storage Components

The platform should conceptually contain five primary persistence areas:

1. Application Store — users, roles, scenarios, workflows.
2. Domain Store — governed reference and regulatory entities.
3. Knowledge Graph — semantic relationships and graph reasoning structures.
4. Search/Vector Index — full-text and semantic retrieval projections.
5. Document/Object and Analytical Stores — source artifacts and high-volume trade observations.

## 4. Logical Data Ownership

| Data | Authoritative Logical Store | Possible Projections |
|---|---|---|
| User | Application Store | Search/audit |
| Role/Permission | Application Store | Authorization cache |
| Export Scenario | Application Store | Graph projection if useful |
| Product | Domain Store | Graph, search |
| HS Code | Domain Store | Graph, search |
| Country | Domain Store | Graph, search |
| Market/Jurisdiction | Domain Store | Graph, search |
| Agency | Domain Store | Graph, search |
| Regulatory Instrument | Domain Store + document artifact | Graph, search |
| Provision | Domain Store | Graph, search |
| Requirement | Domain Store | Graph, search |
| Agreement | Domain Store + document artifact | Graph, search |
| Preference | Domain Store | Graph |
| Tariff | Trade/market-access store | Graph projection, search |
| NTM | Domain/market-access store | Graph, search |
| Source | Domain Store | Graph |
| Document | Object Store | Metadata/search/graph |
| Dataset | Data Store | Graph/search metadata |
| Data Record | Analytical Store | Selected graph projections |
| Assertion | Domain/knowledge store | Graph/search |
| Evidence Record | Domain/knowledge store | Graph |
| Finding | Application/knowledge store | Graph/search where useful |

The table defines logical ownership, not necessarily one physical database.

## 5. Application Data Model

Application data represents operational state.

Core entities:

- User
- Role
- Permission
- Organization
- UserRole
- RolePermission
- ExportScenario
- ScenarioInput
- ScenarioResult
- SavedResearch
- AlertSubscription
- Report
- WorkflowTask
- Notification
- AuditEvent.

This data is generally relational because it requires transactions, constraints, authorization, predictable queries and lifecycle management.

## 6. Domain Reference Model

Candidate domain entities include:

- product
- product_attribute
- hs_nomenclature
- hs_code
- hs_code_mapping
- country
- market
- agency
- regulatory_instrument
- provision
- requirement
- requirement_condition
- agreement
- agreement_party
- preference
- preference_condition
- ntm
- tariff
- document_type
- regulatory_topic.

The exact schema will be refined during implementation design.

## 7. Primary Key Strategy

Every persistent entity should have a stable internal identifier.

External identifiers should be represented separately.

Example:

    entity
      ├── id = internal stable ID
      └── external_identifier
            ├── source
            ├── identifier
            └── identifier_type

This prevents external systems from becoming the platform's only identity mechanism.

## 8. Composite / Natural Keys

Natural keys remain useful for uniqueness constraints.

Examples:

- HS Code: (nomenclature_id, version_id, code)
- Country: (ISO standard, code)
- Dataset Record: (dataset_id, source_record_id)

Natural keys should not automatically replace internal IDs. They are particularly useful for preventing duplicate ingestion.

## 9. Regulatory Instrument Storage

A regulatory instrument should have structured metadata separate from its content artifact.

    regulatory_instrument
        │
        ├── metadata
        ├── provisions
        ├── lifecycle
        ├── temporal validity
        └── document references
                  │
                  ▼
            document/object store

This allows metadata queries without opening the underlying document.

## 10. Provision Storage

A provision should be independently addressable.

Candidate fields:

- id
- instrument_id
- parent_provision_id
- provision_type
- provision_number
- heading
- text
- source_location
- sequence
- valid_from
- valid_to.

A hierarchical provision structure allows Article → Section → Subsection → Paragraph, while recognizing that legal hierarchies vary by instrument.

## 11. Requirement Storage

A Requirement should be separated from the provision that establishes it.

    requirement
        │
        ├── description
        ├── type
        ├── status
        ├── temporal validity
        │
        └── requirement_provision
                  │
                  ▼
               provision

Applicability conditions should not be buried in free text where deterministic evaluation is possible.

Potential condition components:

- product/HS condition
- origin condition
- destination condition
- date condition
- quantity condition
- processing condition
- exporter condition
- agreement condition.

## 12. Applicability Persistence

Applicability should be represented separately from the requirement definition.

    requirement
          ↓
    applicability_rule
          ├── conditions
          ├── result semantics
          ├── valid period
          └── evidence

An evaluated scenario may produce:

    scenario
        ↓
    applicability_evaluation
        ↓
    requirement
        ↓
    Applicable / Not Applicable / Unresolved

This prevents a permanent requirement record from being confused with a scenario-specific evaluation.

## 13. Agreement and Preference Storage

Agreement:

    agreement
      ├── agreement_party
      ├── provision
      ├── product/HS coverage
      └── preference

Preference:

    preference
      ├── agreement_id
      ├── origin
      ├── destination
      ├── product/HS scope
      ├── rate/condition
      └── eligibility rules

The relationship between agreement and preference must remain explicit.

## 14. Tariff Storage

Tariff data should support both base and preferential conditions.

Candidate conceptual fields:

- id
- dataset_id
- hs_code_id
- origin_regime
- destination_market_id
- tariff_type
- rate
- unit
- quota_reference
- valid_from
- valid_to
- source_record_id.

Where tariff data is high-volume, detailed observations should remain in an analytical data store rather than being unnecessarily duplicated as graph nodes.

## 15. Trade Data Model

Trade data is naturally suited to a dimensional/analytical model.

Conceptually:

    Reporter ─┐
    Partner ───┼──> Trade Fact <── Product/HS
    Period ────┘

Potential dimensions:

- reporter
- partner
- product/HS
- period
- trade direction
- geography
- currency/value convention
- dataset.

Potential measures:

- trade value
- quantity
- unit value
- calculated indicators.

## 16. Trade Data Quality

Trade records should preserve data-status information.

Possible states:

- observed
- estimated
- provisional
- revised
- missing
- suppressed
- conflicting
- unavailable.

Important rule:

    missing ≠ zero
    estimated ≠ observed
    suppressed ≠ zero

The analytical layer should preserve these distinctions.

## 17. Dataset and Ingestion Model

Candidate operational entities:

- data_source
- dataset
- dataset_version
- ingestion_job
- ingestion_run
- source_record
- validation_result
- data_quality_issue.

Conceptual flow:

    Source
      ↓
    Dataset
      ↓
    Dataset Version
      ↓
    Ingestion Run
      ↓
    Raw/Source Records
      ↓
    Validation
      ↓
    Canonical Records
      ↓
    Analytical Store
      ↓
    Graph/Search Projections

This creates reproducibility and makes upstream changes auditable.

## 18. Document / Object Storage Boundary

Binary artifacts should be stored separately from relational metadata.

Examples:

- PDF
- scanned gazette
- DOC/DOCX
- spreadsheet
- HTML snapshot
- image
- OCR artifact.

Logical metadata:

- id
- source_id
- title
- document_type
- publication_date
- acquisition_date
- checksum
- storage_reference
- processing_status
- OCR_status.

The binary artifact is referenced through storage_reference.

## 19. Document Processing Model

Document processing may create derived artifacts:

    Original Document
          ↓
    Text Extraction
          ↓
    OCR where required
          ↓
    Structural Segmentation
          ↓
    Instrument Detection
          ↓
    Provision Extraction
          ↓
    Entity/Relationship Extraction
          ↓
    Validation
          ↓
    Published Knowledge

Each processing stage should be traceable.

The original artifact must remain distinguishable from extracted text and derived knowledge.

## 20. Provenance Persistence

Provenance should be queryable without relying exclusively on application logs.

Candidate entities:

- source
- document
- dataset
- evidence_record
- assertion
- assertion_evidence
- derived_relationship.

A provenance chain should be reconstructable:

    Finding
      ↓
    Assertion
      ↓
    Evidence
      ↓
    Provision / Data Record
      ↓
    Document / Dataset
      ↓
    Source

## 21. Temporal Persistence

Temporal fields should be explicit where relevant:

- valid_from
- valid_to
- effective_from
- effective_to
- published_at
- retrieved_at
- amended_at
- superseded_at
- observation_period.

Where the distinction between system time and domain validity becomes important, the implementation should support both.

A record may therefore have a platform retrieval date of 2026-09-19 while having a legal effective date of 2026-07-01. These must not be conflated.

## 22. Knowledge Graph Projection

The graph should generally be treated as a semantic projection of governed domain data.

    Relational/domain records
            ↓
    Projection process
            ↓
    Knowledge Graph

Possible graph nodes:

- Product
- HS Code
- Country
- Market
- Agency
- Instrument
- Provision
- Requirement
- Agreement
- Preference
- Tariff
- NTM
- Source
- Document
- Dataset
- Assertion
- Evidence.

Possible graph edges include classified_as, maps_to, applies_to, applies_in, contains, issued_by, administered_by, derived_from, supports, references, amends, supersedes, participates_in, covers, provides and requires.

## 23. Graph Projection Rules

Every projected graph object should have enough identity information to map back to its authoritative record.

    Graph Node
      ├── internal_id
      ├── entity_type
      └── source_record_reference

Projection jobs should be idempotent. If the same source/domain record is projected twice, it should not create uncontrolled duplicate semantic entities.

## 24. Search Index Boundary

Search is a derived retrieval layer.

It should support:

- full-text document search
- provision search
- instrument search
- product search
- requirement search
- semantic/vector retrieval
- filtering by jurisdiction
- filtering by date
- filtering by source
- filtering by instrument type
- filtering by product/HS.

Search indexes should preserve identifiers that allow retrieval back to authoritative records.

## 25. Vector / Semantic Retrieval

Vector representations should be treated as derived artifacts.

    Authoritative Text
          ↓
    Chunking
          ↓
    Embedding
          ↓
    Vector Index

The embedding itself is not authoritative knowledge.

If source content changes, affected embeddings must be identifiable and regenerable.

## 26. Cache and Read Models

Caches should not become authoritative.

Potential cached/read-model data includes frequently requested tariff results, common product classifications, common market summaries, search result pages, graph traversal results and AI retrieval context.

Every cache entry should have a defined invalidation or freshness strategy.

## 27. Transaction Boundaries

Transactions should protect changes that must remain internally consistent.

### Publishing regulatory knowledge

Instrument metadata, provisions, source references and status change should publish atomically from the application's perspective.

### Ingestion

Dataset version, ingestion run and validation status should maintain consistent processing state.

### Scenario analysis

Scenario inputs should be preserved independently from derived results so that results can be regenerated.

## 28. Data Lifecycle

A governed data lifecycle should look like:

    Acquire
      ↓
    Store Raw
      ↓
    Validate
      ↓
    Normalize
      ↓
    Enrich
      ↓
    Review
      ↓
    Publish
      ↓
    Project
      ↓
    Monitor
      ↓
    Supersede / Retire

Raw source material should not be overwritten by normalized or AI-derived representations.

## 29. Storage Consistency Model

The platform will likely use multiple persistence mechanisms. Therefore consistency should be explicitly classified.

### Strong consistency

Use where required for:

- permissions
- user/role relationships
- workflow transitions
- publication state
- authoritative metadata.

### Eventual consistency

Acceptable for:

- search indexes
- graph projections
- embeddings
- caches
- analytical aggregates.

The user-facing system should indicate when a derived index is temporarily behind the authoritative source if this could affect correctness.

## 30. Data Ownership Matrix

Each domain class should eventually have an explicit owner.

| Domain | Authority |
|---|---|
| Regulatory artifact | Source/Object Store |
| Regulatory metadata | Domain Store |
| Legal provisions | Domain Store |
| Derived requirements | Domain/Knowledge Store |
| Search representation | Search Index |
| Graph representation | Knowledge Graph |
| Trade observations | Analytical Store |
| Scenario | Application Store |
| AI answer | Derived/transient result |
| Audit event | Audit Store |

The AI response itself should not become authoritative merely because it was saved.

## 31. Recommended Logical Architecture

    ┌──────────────────────┐
    │   APPLICATION STORE  │
    │ users/scenarios/etc. │
    └──────────┬───────────┘
               │
    ┌──────────▼───────────┐
    │     DOMAIN STORE     │
    │ governed entities    │
    └─────┬────────┬───────┘
          │        │
    ┌─────▼─────┐  ┌──▼──────────────┐
    │ KNOWLEDGE │  │ SEARCH / VECTOR │
    │   GRAPH   │  │ retrieval layer │
    └───────────┘  └─────────────────┘

    ┌───────────────────────────────────┐
    │          DOCUMENT STORE           │
    │ source artifacts / OCR / files   │
    └───────────────────────────────────┘

    ┌───────────────────────────────────┐
    │       ANALYTICAL TRADE DATA       │
    │ high-volume observations          │
    └───────────────────────────────────┘

This is the current logical storage target.

## 32. What This Pass Establishes

1. Storage responsibilities are separated by workload and authority.
2. Domain data has an authoritative logical owner.
3. Graph and search are primarily derived semantic/retrieval projections.
4. Documents are separate from document metadata.
5. Trade data is separated from transactional application data.
6. High-volume trade observations do not need to become graph nodes.
7. Provenance is persisted as domain knowledge, not merely logs.
8. Temporal validity is explicit.
9. Raw source material is preserved.
10. Derived representations should be rebuildable.
11. Strong and eventual consistency boundaries are explicit.
12. Technology selection should follow these requirements.

## 33. Technology Selection Gate

Technology should now be evaluated against this logical model.

The next decision pass should compare candidate technologies for:

- relational storage
- graph storage
- object/document storage
- full-text/vector search
- analytical trade-data storage
- event/queue infrastructure where needed
- caching.

The comparison should be based on:

- domain fit
- correctness
- query capabilities
- temporal support
- provenance
- scale
- operational complexity
- security
- interoperability
- cost
- developer ecosystem
- portability
- institutional/government deployment considerations.

No technology should be selected solely because it is popular or convenient.
