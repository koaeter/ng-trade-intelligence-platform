# Pass 10 — Source Acquisition, Ingestion & Knowledge Lifecycle

## 1. Purpose

This pass defines how authoritative trade and regulatory information enters the platform, becomes structured knowledge, and remains current over time.

The ingestion architecture must preserve the distinction between:

- the original source
- acquired artifacts
- extracted text
- normalized domain entities
- candidate knowledge
- reviewed knowledge
- published knowledge
- derived search/graph/vector representations.

The system must never overwrite authoritative source material with derived interpretations.

---

# 2. Knowledge Supply Chain

The platform's core knowledge lifecycle is:

```text
Source Discovery
      ↓
Source Registration
      ↓
Acquisition
      ↓
Raw Artifact Storage
      ↓
Validation
      ↓
Extraction / OCR
      ↓
Document Segmentation
      ↓
Entity / Provision Extraction
      ↓
Relationship / Rule Candidate Extraction
      ↓
Normalization
      ↓
Validation
      ↓
Human Review
      ↓
Publication
      ↓
Graph / Search / Vector Projection
      ↓
Monitoring
      ↓
Change Detection
      ↓
Reprocessing / Supersession
```

Each stage must have traceable state.

---

# 3. Source Registry

Every external source should first be represented in the source registry.

Candidate source metadata:

- source_id
- source_name
- organization
- source_type
- jurisdiction
- authority_level
- official_url
- access_method
- access_frequency
- authentication_requirement
- terms_of_use
- expected_format
- update_frequency
- status
- last_successful_acquisition
- last_checked_at.

Possible source types:

- government website
- government API
- international organization
- treaty repository
- legislation database
- customs/tariff database
- trade statistics API
- standards repository
- official publication
- institutional database.

The source registry should not assume that all sources are equally authoritative.

---

# 4. Source Authority

Authority should be represented as metadata.

Conceptual levels:

```text
Primary authoritative
Official secondary
International authoritative
Institutional
Curated reference
Analytical
Unverified / unknown
```

This is not a universal legal hierarchy.

A source can be authoritative for one type of information while not being authoritative for another.

Example:

- an agency may be authoritative for its own procedure
- a trade database may be authoritative for its published dataset
- legislation may be authoritative for the legal provision itself.

---

# 5. Acquisition Methods

The ingestion framework should support multiple acquisition methods.

## 5.1 Web acquisition

For public web pages:

```text
Source
 ↓
URL
 ↓
HTTP acquisition
 ↓
Raw response
 ↓
Artifact
```

Store:

- URL
- retrieval timestamp
- HTTP metadata where useful
- checksum
- content type
- response status
- source identifier.

## 5.2 API acquisition

For structured external APIs:

```text
Source API
 ↓
API request
 ↓
Raw response
 ↓
Source records
 ↓
Normalization
```

Preserve:

- endpoint/resource
- request parameters where appropriate
- retrieval time
- API version
- response metadata
- source record identifiers.

## 5.3 File acquisition

Examples:

- PDF
- DOCX
- XLSX
- CSV
- XML
- JSON
- ZIP.

Original files should be retained where legally and operationally permissible.

## 5.4 Manual acquisition

Some official documents may only be obtainable manually.

Manual uploads should enter the same lifecycle as automated acquisitions.

The system should record:

- who acquired it
- when
- source claimed
- source URL/reference
- file checksum
- review state.

Manual acquisition must not bypass provenance.

---

# 6. Raw Artifact Principle

The original artifact should be preserved.

```text
ORIGINAL
   ↓
immutable / controlled artifact
   ↓
derived processing
```

Never replace the original PDF with OCR text.

Never overwrite a source spreadsheet with normalized values.

Never replace an API response with transformed data.

Derived representations should point back to the original.

---

# 7. Content Integrity

Every acquired artifact should receive an integrity identifier.

Preferred mechanism:

- cryptographic checksum/hash.

Candidate metadata:

- checksum_algorithm
- checksum
- acquired_at
- artifact_size
- media_type.

This allows the system to determine whether an apparently identical document has actually changed.

---

# 8. Deduplication

Duplicate detection should operate at multiple levels.

## Exact duplicate

Same checksum.

## Same source reference

Same source identifier or URL.

## Probable duplicate

Different artifact but substantially identical content.

Probable duplicates must not automatically be deleted.

They should be linked as possible duplicates and reviewed according to source/lifecycle rules.

---

# 9. Document Processing Pipeline

For documents:

```text
Raw Document
      ↓
File Validation
      ↓
Text Extraction
      ↓
OCR if required
      ↓
Structural Detection
      ↓
Section / Provision Segmentation
      ↓
Metadata Extraction
      ↓
Entity Extraction
      ↓
Relationship Candidate Extraction
      ↓
Rule Candidate Extraction
      ↓
Validation
```

Each stage should produce a processing record.

---

# 10. OCR

OCR should be treated as a transformation, not as the authoritative source.

Store:

- OCR engine/version
- processing timestamp
- OCR confidence where available
- page association
- extracted text
- processing errors.

Where possible, preserve page/region references so extracted claims can be traced to the original visual document.

---

# 11. Document Segmentation

Legal and regulatory documents should not be treated as undifferentiated text.

The system should attempt to identify:

- title
- preamble
- chapters
- parts
- sections
- articles
- clauses
- schedules
- annexes
- tables
- footnotes
- appendices.

The exact hierarchy must remain flexible because legal documents differ structurally.

---

# 12. Provision Extraction

A provision record should preserve its relationship to the source document.

Conceptually:

```text
Document
  ↓
Page
  ↓
Section / Article
  ↓
Provision
  ↓
Text
```

Candidate extracted metadata:

- provision number
- heading
- provision type
- parent provision
- source page
- source location
- extracted text
- extraction method
- extraction confidence
- review status.

AI extraction should create candidate provisions rather than automatically publishing them.

---

# 13. Entity Extraction

Candidate entities include:

- products
- HS codes
- countries
- agencies
- agreements
- regulatory instruments
- certificates
- procedures
- requirements
- standards
- organizations
- dates
- rates
- quantities
- thresholds.

Entity extraction should distinguish:

**Mention**

from:

**Confirmed domain entity.**

Example:

A document mentioning "cocoa" does not automatically establish that the document applies to every cocoa product.

---

# 14. Relationship Extraction

The ingestion system may identify candidate relationships such as:

- instrument amends instrument
- instrument supersedes instrument
- provision references provision
- requirement applies to product
- requirement administered by agency
- agreement covers HS code
- preference applies to market
- document describes requirement.

These become candidate assertions.

They must retain:

- extraction method
- source location
- evidence
- extraction confidence
- review status.

---

# 15. Rule Extraction

Some regulatory text can be converted into structured applicability rules.

Example source language:

```text
Products classified under HS 1801
exported to Market X
must satisfy Condition Y.
```

Candidate structured rule:

```text
IF
    HS Code IN 1801
    AND Destination = Market X
THEN
    Requirement = Y
```

The extraction process must preserve the original provision.

The structured rule is a derived interpretation until validated.

---

# 16. Candidate Knowledge vs Published Knowledge

This distinction is fundamental.

```text
RAW
 ↓
EXTRACTED
 ↓
CANDIDATE
 ↓
REVIEWED
 ↓
PUBLISHED
```

Only published knowledge should normally participate in authoritative deterministic evaluations.

Candidate knowledge may be used for:

- reviewer interfaces
- discovery
- internal analysis
- quality checks.

It should not silently become production truth.

---

# 17. Validation Layers

Validation should occur at multiple levels.

## 17.1 Technical validation

Examples:

- valid file
- valid encoding
- valid JSON/XML/CSV
- required fields present
- checksum generated.

## 17.2 Structural validation

Examples:

- valid document structure
- valid provision hierarchy
- valid dataset schema
- valid HS format.

## 17.3 Domain validation

Examples:

- HS code exists in the relevant nomenclature
- country code is recognized
- agency exists
- agreement party exists
- requirement references valid entities.

## 17.4 Temporal validation

Examples:

- effective_from precedes effective_to
- historical versions do not overlap incorrectly
- amendment dates are coherent.

## 17.5 Provenance validation

Every published fact/rule should have a traceable source path.

---

# 18. Human Review

Human review is required for knowledge that can materially affect regulatory conclusions.

Review may be required for:

- legal instrument identification
- provision extraction
- applicability rules
- agreement interpretation
- preference eligibility rules
- origin rules
- tariff mappings
- ambiguous classifications
- conflicting sources.

Review states:

```text
Pending Review
 ↓
Reviewed
 ↓
Approved
 ↓
Published
```

Possible rejection path:

```text
Pending Review
 ↓
Rejected
 ↓
Corrected / Reprocessed
```

---

# 19. Review Prioritization

Not every extracted fact requires identical review effort.

Priority should consider:

- legal significance
- source authority
- uncertainty
- potential user impact
- number of affected products/markets
- regulatory change significance
- extraction quality
- conflict status.

A minor metadata correction should not necessarily block an entire dataset.

---

# 20. Publication

Publication should be a controlled transaction.

Conceptually:

```text
Candidate Knowledge
      ↓
Validation
      ↓
Review Approval
      ↓
Publication Transaction
      ↓
Published Domain Knowledge
      ↓
Projection Jobs
```

Publication should update:

- knowledge status
- version
- provenance
- effective dates
- review metadata.

Then trigger downstream projections.

---

# 21. Projection Lifecycle

Published knowledge feeds derived representations.

```text
Published Domain Knowledge
          │
     ┌────┼──────────┐
     ↓    ↓          ↓
   Graph Search   Vector
     │    │          │
     └────┴──────────┘
          ↓
       Retrieval
```

These projections are rebuildable.

The domain store remains authoritative.

---

# 22. Idempotent Processing

Processing stages should be idempotent where practical.

If the same source is processed twice:

- it should not create duplicate authoritative entities
- it should not corrupt relationships
- it should not produce uncontrolled duplicate embeddings
- it should be possible to identify the processing run.

Stable identifiers and deterministic keys are therefore important.

---

# 23. Change Detection

The platform should detect changes at several levels.

## Artifact change

Checksum changes.

## Document change

Text/content changes.

## Provision change

A specific provision changes.

## Metadata change

Effective date/status/title changes.

## Relationship change

Amendment/supersession/coverage changes.

## Dataset change

Records added, removed, revised or corrected.

Change detection should identify the smallest meaningful changed unit where possible.

---

# 24. Regulatory Change Pipeline

```text
Source Checked
      ↓
New / Changed Artifact
      ↓
Artifact Diff
      ↓
Document Diff
      ↓
Provision Diff
      ↓
Affected Knowledge
      ↓
Affected Requirements
      ↓
Affected Products / Markets
      ↓
Impact Analysis
      ↓
Review
      ↓
Publish
      ↓
Alerts
```

This is a core future capability of the platform.

---

# 25. Amendment and Supersession Detection

Possible signals:

- explicit amendment language
- "amended by"
- "repealed by"
- "superseded by"
- replacement document
- changed effective date
- official publication notice.

AI can identify candidate relationships.

The system should validate them against source evidence before publication.

---

# 26. Reprocessing

When processing logic changes, the system should be able to reprocess historical artifacts.

Example:

```text
Original PDF
     ↓
Processing Run V1
     ↓
Knowledge V1
     
New extraction logic
     ↓
Same Original PDF
     ↓
Processing Run V2
     ↓
Knowledge V2
```

Do not destroy the historical processing record.

This allows:

- comparison
- regression testing
- debugging
- audit
- controlled migration.

---

# 27. Data Quality States

A source or dataset can have different quality conditions.

Possible states:

- valid
- incomplete
- stale
- estimated
- provisional
- conflicting
- malformed
- unavailable
- deprecated.

These states should be distinct from business applicability.

For example:

`Data quality = provisional`

does not automatically mean:

`Requirement = not applicable`.

---

# 28. Freshness

Freshness should be represented explicitly.

Candidate metadata:

- source_last_checked_at
- source_last_changed_at
- retrieved_at
- published_at
- effective_from
- effective_to
- freshness_status.

Possible freshness states:

- current
- recently_checked
- stale
- unknown.

Freshness must not be confused with legal validity.

A document can be legally valid but not recently retrieved.

---

# 29. Source Outage Handling

External sources will sometimes be unavailable.

The system should:

- retain last successful acquisition
- record outage
- avoid falsely marking data as changed
- expose source freshness
- retry according to source-specific policy
- alert operators when freshness thresholds are exceeded.

Cached/stored source data remains usable according to its known validity, but the UI should make freshness visible when relevant.

---

# 30. External API Ingestion

API connectors should handle:

- authentication
- pagination
- rate limits
- retries
- timeouts
- API version changes
- schema changes
- partial responses
- upstream errors
- duplicate records
- revised records.

Each ingestion run should retain enough metadata to reproduce what was retrieved.

---

# 31. Source-Specific Adapters

Do not make the entire ingestion engine understand every external source format.

Use source adapters:

```text
Ingestion Framework
      │
      ├── Nigeria Source Adapter
      ├── WTO Adapter
      ├── ITC Adapter
      ├── UN/International Dataset Adapter
      └── Generic File Adapter
```

Adapters translate source-specific structures into canonical platform structures.

---

# 32. Canonical Data Model

External source fields should not leak directly into domain logic.

Example:

```text
External API
   ↓
Source Adapter
   ↓
Canonical Trade Record
   ↓
Domain / Analytical Store
```

This protects the rest of the application when an external provider changes field names or response structures.

---

# 33. Ingestion Observability

Each processing stage should expose operational metrics such as:

- records received
- records processed
- records accepted
- records rejected
- processing duration
- extraction errors
- validation errors
- review backlog
- publication count
- projection failures.

Operational logs should include:

- ingestion run ID
- source ID
- artifact ID
- processing stage
- correlation/request ID where applicable.

---

# 34. Failure Isolation

A failed source should not necessarily stop the entire platform.

For example:

```text
WTO ingestion       ✓
ITC ingestion       ✓
Nigeria source A    ✓
Nigeria source B    ✗
UN dataset          ✓
```

The platform should continue operating while clearly exposing the affected source's freshness/state.

Similarly, a failed graph projection should not invalidate the authoritative relational knowledge.

---

# 35. Knowledge Lifecycle State Model

A source-derived knowledge item can move through:

```text
Discovered
    ↓
Acquired
    ↓
Validated
    ↓
Processed
    ↓
Reviewed
    ↓
Published
    ↓
Superseded
    ↓
Retired
```

Not every artifact must pass through identical stages.

For example, a trusted structured API may require less manual review than a scanned legal document.

---

# 36. Provenance Chain

The minimum provenance chain should be:

```text
Claim / Finding
      ↓
Assertion
      ↓
Evidence Record
      ↓
Provision / Data Record
      ↓
Document / Dataset
      ↓
Source
```

For extracted knowledge:

```text
Published Requirement
      ↓
Rule Candidate
      ↓
Provision
      ↓
Document Location
      ↓
Original Artifact
      ↓
Source
```

Every transformation should remain traceable.

---

# 37. Security Considerations

Ingestion is a major security boundary.

Controls should include:

- malware/file scanning where appropriate
- content-type validation
- size limits
- controlled processing environments
- sandboxing for untrusted documents
- least-privilege source credentials
- secret management
- audit logging
- restricted publication permissions.

External content should never be treated as trusted executable content.

---

# 38. Prompt-Injection Consideration

Regulatory documents may contain text that is processed by an LLM.

The ingestion pipeline must treat source text as **data**, not instructions to the model.

For example, text extracted from a document saying:

```text
"Ignore previous instructions..."
```

must not alter the system's processing policy.

The AI extraction layer should operate under explicit system constraints and return structured candidates rather than executing document instructions.

This is particularly important for a platform that processes arbitrary external documents.

---

# 39. Source Conflict Management

Different official sources may contain inconsistent information.

The ingestion system should not automatically overwrite one source with another.

Instead:

```text
Source A → Assertion A
Source B → Assertion B
              ↓
          Conflict Set
              ↓
       Resolution Workflow
              ↓
   Resolved / Unresolved
```

The resolution decision should itself have provenance.

---

# 40. Knowledge Retirement

Retirement should not mean deletion.

When knowledge is no longer active:

- preserve the historical record
- mark it superseded/retired
- preserve validity dates
- preserve source references
- remove it from current applicability where appropriate
- retain it for historical queries.

Historical regulatory intelligence is a core capability.

---

# 41. Rebuildability

Derived stores should be rebuildable from authoritative data.

This applies to:

- graph
- search index
- embeddings
- caches
- analytical aggregates where possible.

Ideal architecture:

```text
Authoritative Store
        ↓
Projection Pipeline
        ↓
Derived Stores
```

If a derived store is lost, it should be possible to regenerate it.

---

# 42. Publication Safety

Before a knowledge item becomes available to deterministic evaluation, verify:

- source exists
- source artifact exists
- provenance is complete
- temporal metadata is valid
- entity references resolve
- required review is complete
- conflicts are resolved or explicitly marked
- version is established.

Only then:

`status = PUBLISHED`

---

# 43. Initial Ingestion Pipeline

The first practical implementation can use:

```text
SOURCE
  ↓
Acquisition
  ↓
Raw Artifact
  ↓
Metadata Extraction
  ↓
Text / Data Extraction
  ↓
Normalization
  ↓
Candidate Knowledge
  ↓
Validation
  ↓
Review
  ↓
Publication
  ↓
PostgreSQL
  ↓
pgvector / Search / Graph projections
```

This pipeline is sufficient to begin building the first real ingestion workflows without prematurely introducing a distributed event architecture.

---

# 44. First Source Categories

The platform should eventually prioritize source categories rather than attempting to ingest the entire internet.

Initial categories:

### Nigerian regulatory sources

- laws and regulations
- export procedures
- agency requirements
- standards/certification requirements
- customs/tariff information
- official trade notices
- export-related circulars/guidelines.

### International/regional sources

- WTO
- ITC
- UN trade/statistical sources
- AfCFTA
- ECOWAS
- bilateral/regional agreements
- destination-market official sources.

Each source should enter the registry before ingestion.

---

# 45. Source Onboarding Workflow

```text
Identify Source
      ↓
Assess Authority
      ↓
Register Source
      ↓
Define Acquisition Method
      ↓
Test Acquisition
      ↓
Validate Output
      ↓
Configure Schedule
      ↓
Enable Ingestion
      ↓
Monitor
```

Source onboarding itself should be auditable.

---

# 46. First-Release Knowledge Lifecycle

For the first release, avoid trying to automate everything.

Recommended initial lifecycle:

```text
Acquire
  ↓
Validate
  ↓
Extract
  ↓
Normalize
  ↓
Human Review
  ↓
Publish
  ↓
Project
```

Automation can increase gradually as confidence and test coverage improve.

---

# 47. Key Architectural Decision

**Authoritative sources remain the root of the knowledge supply chain.**

AI extraction, graph construction, embeddings and search indexing are downstream transformations.

Therefore:

```text
Source
  ↓
Canonical / governed data
  ↓
Derived knowledge
  ↓
AI retrieval
  ↓
AI response
```

not:

```text
AI response
  ↓
"knowledge"
```

---

# 48. Next Pass

**Pass 11 — API & Service Architecture**

The next pass should define how the web application communicates with the domain, data, AI and ingestion layers.

It should cover:

- API boundaries
- domain services
- application services
- command/query separation
- request/response models
- authentication/authorization boundaries
- scenario analysis API
- search API
- AI assistant API
- evidence API
- ingestion API
- administrative API
- asynchronous jobs
- error model
- versioning
- idempotency
- API security
- observability.

This will give us the application's actual service/API structure before implementation begins.