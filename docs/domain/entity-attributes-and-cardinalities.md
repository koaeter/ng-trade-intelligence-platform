# Entity Attributes, Identifiers & Cardinalities

## 1. Purpose

This document converts the conceptual domain model into a more precise logical model.

It defines:

- stable identifiers
- important attributes
- required vs optional information
- relationship cardinalities
- lifecycle/status concepts
- temporal fields
- provenance requirements.

It remains technology-neutral. It does not prescribe a specific database, graph engine, ORM or API framework.

---

## 2. Identifier Principles

Every persistent domain entity should have a stable internal identifier.

Recommended conceptual pattern:

```text
<Entity Type>:<stable identifier>
```

Examples:

```text
product:...
country:NG
hs-code:HS2022:0901.11
instrument:...
provision:...
agreement:...
requirement:...
```

Internal identifiers must not depend exclusively on:

- display names
- URLs
- document filenames
- mutable source identifiers.

External identifiers should be stored separately.

### Identifier categories

| Identifier | Purpose |
|---|---|
| Internal ID | Stable platform identity |
| External ID | Identifier assigned by an upstream source |
| Version ID | Identity of a specific version |
| Natural Key | Domain combination that may identify a record |
| Source Record ID | Identifier used by a particular dataset/source |

The same external identifier may mean different things across sources, so source context should accompany external identifiers.

---

# 3. Common Metadata

Most persistent entities should support, where appropriate:

- internal ID
- created-at
- updated-at
- lifecycle/status
- provenance reference
- source reference
- effective-from
- effective-to.

Not every entity requires every field.

Operational metadata such as ingestion timestamps should not be confused with legal or commercial effective dates.

---

# 4. Product

## Core attributes

| Attribute | Required | Description |
|---|---|---|
| id | Yes | Stable product identifier |
| name | Yes | Human-readable product name |
| description | Recommended | Detailed description |
| product category | Optional | Domain/sector classification |
| attributes | Optional | Structured product characteristics |
| processing state | Optional | Raw, processed, manufactured, etc. |
| intended use | Optional | Relevant intended use |
| status | Yes | Active, deprecated, etc. |

## Relationships

```text
Product 1 ──── 0..* HS Classification
Product 1 ──── 0..* Requirement
Product 1 ──── 0..* Trade Data Records
Product 1 ──── 0..* Export Scenarios
```

A Product may have multiple candidate HS classifications.

---

# 5. HS Classification

Rather than treating an HS code as a standalone number, model a classification concept within a nomenclature.

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| nomenclature | Yes |
| version/year | Yes |
| code | Yes |
| description | Yes |
| level | Yes |
| parent classification | Recommended |
| effective-from | Recommended |
| effective-to | Optional |
| source | Yes |

## Relationships

```text
HS Version 1 ──── 1..* HS Codes
HS Code 1 ──── 0..* Product Classifications
HS Code 1 ──── 0..* HS Mappings
HS Code 1 ──── 0..* Tariffs
HS Code 1 ──── 0..* Trade Data Records
```

### Classification mapping

Mappings between HS versions must be explicit.

```text
HS2022:0901.11
      ↓ maps_to
HS2017:0901.11
```

Mappings may be:

- one-to-one
- one-to-many
- many-to-one
- unresolved.

The platform must not assume that identical-looking codes across versions have identical meaning.

---

# 6. Country

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| ISO code(s) | Recommended |
| name | Yes |
| official name | Optional |
| region | Optional |
| status | Yes |

## Relationships

```text
Country 1 ──── 0..* Agreements
Country 1 ──── 0..* Markets/Jurisdictions
Country 1 ──── 0..* Trade Data Records
Country 1 ──── 0..* Regulatory Instruments
```

Country identity should be normalized rather than repeated as arbitrary strings throughout datasets.

---

# 7. Market / Jurisdiction

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| name | Yes |
| type | Yes |
| parent jurisdiction | Optional |
| country relationship | Optional |
| regulatory characteristics | Optional |
| status | Yes |

Possible types:

- country
- customs territory
- regional bloc
- economic area
- special territory
- other recognized trade jurisdiction.

## Relationships

```text
Market 1 ──── 0..* Requirements
Market 1 ──── 0..* Tariffs
Market 1 ──── 0..* NTMs
Market 1 ──── 0..* Agreements
```

---

# 8. Regulatory Instrument

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| title | Yes |
| instrument type | Yes |
| issuing authority | Yes |
| jurisdiction | Yes |
| identifier/number | Recommended |
| publication date | Recommended |
| effective-from | Recommended |
| effective-to | Optional |
| status | Yes |
| version | Recommended |
| language | Optional |
| source | Yes |

## Relationships

```text
Instrument 1 ──── 1..* Provisions
Instrument 1 ──── 0..* Instruments it amends
Instrument 1 ──── 0..* Instruments it supersedes
Instrument 1 ──── 0..* Requirements
Instrument 1 ──── 1..* Sources/Documents
```

Instrument relationships must be explicit and typed.

Examples:

- amends
- amended_by
- repeals
- repealed_by
- supersedes
- superseded_by
- implements
- derives_from
- references.

---

# 9. Provision

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| instrument | Yes |
| provision type | Yes |
| provision number | Recommended |
| heading | Optional |
| text | Yes |
| source location | Recommended |
| effective status | Recommended |

## Relationships

```text
Instrument 1 ──── 1..* Provisions
Provision 1 ──── 0..* Requirements
Provision 1 ──── 0..* Assertions
Provision 1 ──── 0..* Provisions referenced
```

A provision may support multiple derived requirements or assertions.

---

# 10. Requirement

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| requirement type | Yes |
| description | Yes |
| applicability conditions | Yes |
| jurisdiction | Yes |
| responsible agency | Recommended |
| effective-from | Recommended |
| effective-to | Optional |
| status | Yes |
| evidence/document type | Optional |

## Relationships

```text
Requirement 1 ──── 1..* Provisions
Requirement 1 ──── 0..* Products
Requirement 1 ──── 0..* HS Codes
Requirement 1 ──── 0..* Markets
Requirement 1 ──── 0..* Agencies
```

A requirement may be supported by several provisions and may apply to many products.

Applicability should not be encoded merely as a static product-to-requirement link; conditions matter.

---

# 11. Agreement

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| name/title | Yes |
| agreement type | Yes |
| parties | Yes |
| administering/secretariat authority | Optional |
| signature date | Optional |
| entry-into-force date | Recommended |
| termination date | Optional |
| status | Yes |
| source | Yes |

## Relationships

```text
Agreement 1 ──── 2..* Parties
Agreement 1 ──── 0..* Products/HS Codes
Agreement 1 ──── 0..* Preferences
Agreement 1 ──── 0..* Rules of Origin
Agreement 1 ──── 1..* Provisions
```

An agreement may contain many provisions and commercial conditions.

---

# 12. Preference

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| preference type | Yes |
| agreement | Yes |
| beneficiary/origin | Yes |
| destination | Yes |
| product/HS scope | Yes |
| rate/condition | Yes |
| eligibility conditions | Yes |
| effective-from | Yes |
| effective-to | Optional |
| source | Yes |

## Relationships

```text
Agreement 1 ──── 0..* Preferences
Preference 1 ──── 0..* Export Scenarios
Preference 1 ──── 0..* HS Codes
Preference 1 ──── 0..* Rules of Origin
```

A Preference is an available treatment; an Export Scenario determines whether it is applicable.

---

# 13. Tariff

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| HS code | Yes |
| destination | Yes |
| origin regime | Recommended |
| tariff type | Yes |
| rate | Yes |
| unit | Recommended |
| quota relationship | Optional |
| effective-from | Yes |
| effective-to | Optional |
| source dataset | Yes |

## Relationships

```text
HS Code 1 ──── 0..* Tariffs
Market 1 ──── 0..* Tariffs
Tariff 1 ──── 0..* Preferences
```

---

# 14. Non-Tariff Measure

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| measure type | Yes |
| description | Yes |
| HS scope | Recommended |
| origin scope | Recommended |
| destination | Yes |
| responsible authority | Optional |
| effective-from | Recommended |
| effective-to | Optional |
| source | Yes |

## Relationships

```text
NTM 1 ──── 0..* HS Codes
NTM 1 ──── 0..* Requirements
NTM 1 ──── 0..* Markets
```

---

# 15. Export Scenario

Export Scenario is primarily an application/workflow object.

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| product | Yes |
| origin | Yes |
| destination | Yes |
| analysis date | Yes |
| HS classification | Recommended |
| quantity | Optional |
| quantity unit | Optional |
| intended value | Optional |
| exporter context | Optional |
| processing state | Optional |
| origin status | Optional |
| created by | Yes |
| status | Yes |

## Relationships

```text
Export Scenario 1 ──── 1 Product
Export Scenario 1 ──── 1 Origin
Export Scenario 1 ──── 1 Destination
Export Scenario 1 ──── 0..* Requirements
Export Scenario 1 ──── 0..* Tariffs
Export Scenario 1 ──── 0..* Preferences
Export Scenario 1 ──── 0..* Findings
Export Scenario 1 ──── 0..* Evidence Records
```

The scenario should preserve the inputs used for an analysis so that results can be reproduced.

---

# 16. Source

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| name | Yes |
| authority | Yes |
| source type | Yes |
| canonical location | Recommended |
| authority level | Recommended |
| access method | Recommended |
| update frequency | Optional |
| status | Yes |

Possible source types:

- government portal
- legislation repository
- official publication
- treaty repository
- API
- statistical database
- international organisation
- institutional database.

---

# 17. Document

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| source | Yes |
| title | Yes |
| document identifier | Optional |
| document type | Yes |
| publication date | Optional |
| language | Recommended |
| version | Optional |
| acquisition date | Yes |
| content location | Yes |
| checksum/integrity hash | Recommended |
| processing status | Yes |
| OCR status | Optional |

## Relationships

```text
Source 1 ──── 0..* Documents
Document 1 ──── 0..* Instruments
Document 1 ──── 0..* Provisions
Document 1 ──── 0..* Evidence Records
```

A single document can contain multiple related information objects.

---

# 18. Dataset

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| source | Yes |
| name | Yes |
| provider | Yes |
| version | Recommended |
| classification | Recommended |
| coverage | Yes |
| methodology | Recommended |
| units | Recommended |
| update frequency | Optional |
| retrieval date | Yes |
| status | Yes |

## Relationships

```text
Dataset 1 ──── 1..* Data Records
Dataset 1 ──── 0..* Evidence Records
```

---

# 19. Data Record

## Core attributes

The exact schema depends on the dataset, but trade observations should support, where applicable:

- reporter
- partner
- period
- trade direction
- HS version
- HS code
- quantity
- quantity unit
- trade value
- currency/value convention
- data status
- source record identifier.

## Relationships

```text
Dataset 1 ──── 1..* Data Records
Data Record 1 ──── 0..* Evidence Records
Data Record 1 ──── 0..* Assertions
```

---

# 20. Assertion

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| subject | Yes |
| predicate | Yes |
| object/value | Yes |
| applicability context | Recommended |
| valid-from | Optional |
| valid-to | Optional |
| evidence state | Yes |
| created/derived date | Yes |

Assertions should be machine-readable where practical.

Example:

```text
Subject: requirement:123
Predicate: applies_to
Object: hs-code:HS2022:0901.11
Context: destination:DE
Valid: 2026-01-01 → ...
State: Confirmed
```

---

# 21. Evidence Record

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| evidence type | Yes |
| source | Yes |
| document/dataset | Recommended |
| provision/data record | Optional |
| location | Recommended |
| extracted content | Optional |
| retrieval date | Yes |
| evidence state | Yes |

Evidence should be precise enough to support audit and user inspection.

---

# 22. Finding

## Core attributes

| Attribute | Required |
|---|---|
| id | Yes |
| scenario/context | Recommended |
| finding type | Yes |
| statement | Yes |
| supporting assertions | Yes |
| supporting evidence | Yes |
| uncertainty state | Yes |
| generated/derived date | Yes |

A Finding should never be stored without knowing what evidence or assertions support it.

---

# 23. Agency

An Agency represents an organisation responsible for administering, enforcing, issuing, or interpreting a requirement or instrument.

Core attributes:

- id
- name
- jurisdiction
- agency type
- contact/reference information where appropriate
- status
- source.

Relationships:

```text
Agency 1 ──── 0..* Requirements
Agency 1 ──── 0..* Instruments
Agency 1 ──── 0..* Certificates/Documents
```

---

# 24. Cardinality Summary

| Relationship | Cardinality |
|---|---|
| Product → HS Classification | 1 : 0..* |
| HS Code → Tariff | 1 : 0..* |
| Country → Agreement | 1 : 0..* |
| Agreement → Party | 1 : 2..* |
| Agreement → Preference | 1 : 0..* |
| Instrument → Provision | 1 : 1..* |
| Provision → Requirement | 1 : 0..* |
| Requirement → Provision | 1 : 1..* |
| Requirement → Product | 1 : 0..* |
| Market → Requirement | 1 : 0..* |
| Source → Document | 1 : 0..* |
| Dataset → Data Record | 1 : 1..* |
| Assertion → Evidence | 1 : 1..* |
| Finding → Assertion | 1 : 1..* |
| Export Scenario → Finding | 1 : 0..* |

These are logical cardinalities, not necessarily direct relational foreign-key relationships.

---

# 25. Lifecycle States

Lifecycle states should be explicit where an entity passes through an operational workflow.

A common knowledge lifecycle is:

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
Superseded / Retired
```

Operational entities may use different states.

The system must distinguish:

- lifecycle state
- legal status
- data quality state
- evidence/uncertainty state.

These are not interchangeable.

---

# 26. Temporal Fields

Where temporal validity matters, use explicit fields rather than embedding dates in free text.

Recommended concepts:

- valid-from
- valid-to
- effective-from
- effective-to
- publication-date
- amendment-date
- repeal-date
- supersession-date
- observation-period
- retrieved-at.

The distinction is important:

```text
published_at
    ≠
effective_from
    ≠
retrieved_at
```

---

# 27. Provenance Requirements

Important derived objects should preserve provenance.

Minimum conceptual chain:

```text
Finding
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

For regulatory facts, provenance should ideally reach the precise provision.

For trade statistics, provenance should reach the relevant dataset and data record or reproducible query/snapshot.

---

# 28. Graph-Oriented Relationships

The following relationships are particularly valuable for graph reasoning:

- classified_as
- maps_to
- applies_to
- applies_in
- administered_by
- contained_in
- contains
- supports
- derived_from
- references
- amends
- supersedes
- repeals
- implements
- participates_in
- covers
- provides
- eligible_under
- measured_by
- reported_by
- traded_with
- targets
- originates_in.

Relationship types should be explicit rather than represented as generic links.

---

# 29. What This Pass Establishes

This pass establishes a logical domain contract before implementation.

The major conclusions are:

1. Stable internal identity is mandatory.
2. External identifiers remain source-specific.
3. Product and classification remain separate.
4. HS classifications are versioned.
5. Requirements are contextual rather than universally applicable.
6. Agreements and preferences are separate.
7. Source, Document, Dataset and Data Record are separate layers.
8. Provisions provide fine-grained legal provenance.
9. Export Scenario preserves analysis context.
10. Assertions and Findings are derived knowledge, not source material.
11. Temporal validity is explicit.
12. Lifecycle, legal status, data quality and uncertainty are separate dimensions.
13. Graph relationships should be typed.
14. The logical model remains independent of implementation technology.

---

# 30. Next Design Questions

The next pass should move from **what entities are** to **how the knowledge itself is represented**.

Recommended Pass 5:

### Knowledge Graph Ontology & Relationship Model

Define:

- node types
- relationship types
- relationship properties
- ontology boundaries
- provenance graph
- temporal graph model
- applicability model
- amendment/supersession graph
- product/classification graph
- agreement/preference graph
- regulatory requirement graph
- trade-data graph boundaries
- which relationships should be inferred vs explicitly stored
- how GraphRAG would traverse this model.

Only after that should we begin designing the relational schema and implementation architecture.
