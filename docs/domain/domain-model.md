# Domain Model

## 1. Purpose

This document defines the conceptual domain model for the NG Trade Intelligence Platform.

It establishes what the platform means by its core objects before implementation technology is selected. It is intentionally technology-neutral.

The model must support:

- regulatory intelligence
- export requirement analysis
- market access analysis
- agreement applicability
- trade-data intelligence
- evidence-backed AI answers
- temporal reasoning
- auditability and provenance.

---

## 2. Core Modeling Principle

The platform should distinguish between:

1. **Things in the trade domain** — products, countries, agreements, requirements, etc.
2. **Authoritative information about those things** — sources, documents, datasets and records.
3. **Interpretations derived from that information** — findings, assessments, analyses and AI responses.
4. **A user's scenario** — the specific product, origin, destination, date and context being analysed.

This prevents the system from confusing a source document with the legal or commercial concept described by that document.

Conceptually:

```text
DOMAIN ENTITY
    ↓
ASSERTION / FACT
    ↓
EVIDENCE
    ↓
SOURCE
```

An AI-generated answer sits above this chain; it does not replace it.

---

## 3. Core Domain Entities

### 3.1 Product

A **Product** is the commercial good being considered for trade.

Examples:

- cocoa beans
- ginger
- sesame seed
- processed food
- machinery.

A Product should not be identified solely by an HS code.

A product may have:

- common/commercial name
- description
- product attributes
- sector/category
- regulatory characteristics
- one or more classification relationships.

### 3.2 HS Code

An **HS Code** is a classification identifier within a particular Harmonized System nomenclature/version.

Important rule:

> An HS code is a versioned classification concept, not simply a permanent number.

The model should therefore retain:

- HS nomenclature/version
- code
- description
- hierarchy
- validity period where applicable
- mappings to other versions
- classification source.

Potential hierarchy:

```text
Section
  ↓
Chapter
  ↓
Heading
  ↓
Subheading
```

National tariff extensions may extend beyond the internationally harmonized level and must be represented separately from the base HS concept.

### 3.3 Country

A **Country** represents a sovereign state or other jurisdiction relevant to trade.

It may participate in:

- export/import transactions
- agreements
- customs territories
- regulatory regimes
- markets.

The model should allow country identity to be distinct from a broader **Market/Jurisdiction** concept because a trade regime may not always map one-to-one to a sovereign country.

### 3.4 Market / Jurisdiction

A **Market/Jurisdiction** represents the regulatory or commercial destination context in which requirements apply.

Examples may include:

- a country
- customs territory
- regional market
- economic bloc
- special regulatory territory.

This abstraction becomes important for regional regimes and non-country regulatory systems.

### 3.5 Regulatory Instrument

A **Regulatory Instrument** is a formal instrument containing authoritative legal, regulatory, policy, procedural or technical content.

The platform must preserve the instrument's type rather than flattening everything into "regulation".

Possible types include:

- Act
- Regulation
- Rule
- Decree/Order
- Directive
- Circular
- Guideline
- Standard
- Procedure
- Notice
- Treaty
- Agreement
- Protocol
- Convention
- MOU
- Policy instrument.

Each instrument should have concepts such as:

- title
- instrument type
- issuing authority
- jurisdiction
- publication date
- effective-from date
- effective-to date
- status
- version
- amendment relationships
- repeal/supersession relationships
- source references.

Legal equivalence must never be inferred merely because two instruments share similar text or subject matter.

### 3.6 Provision

A **Provision** is a meaningful unit of content within an instrument.

Depending on the source, this may correspond to:

- article
- section
- subsection
- paragraph
- schedule
- annex
- table
- clause.

A provision should retain its location in the source so that an assertion can be traced back to precise evidence.

Conceptually:

```text
Instrument
   └── contains
        └── Provision
             └── supports
                  └── Assertion
```

### 3.7 Requirement

A **Requirement** represents a condition, obligation, restriction, documentation requirement, procedural requirement, technical requirement or other condition relevant to trade.

Examples:

- export permit required
- phytosanitary certificate required
- labelling requirement
- inspection requirement
- restricted product
- conformity assessment required.

A Requirement should capture, where applicable:

- requirement type
- subject/product
- origin
- destination/jurisdiction
- responsible authority
- applicability conditions
- effective period
- severity/importance
- required evidence/document
- source provisions.

A requirement is a **derived domain object** when it is interpreted from one or more authoritative provisions. The system must retain that derivation.

### 3.8 Agreement

An **Agreement** represents an international, regional or bilateral instrument governing relationships between participating parties.

Examples include:

- trade agreements
- preferential trade arrangements
- protocols
- conventions where relevant to trade
- regional integration instruments.

Agreement is related to Regulatory Instrument but has additional trade-specific semantics.

An Agreement may define:

- parties
- covered products
- rules of origin
- tariff preferences
- market-access commitments
- quotas
- exclusions
- implementation dates.

The system must distinguish:

```text
Agreement exists
        ≠
Preference automatically applies
```

Applicability depends on conditions such as product, origin, destination, date and agreement rules.

### 3.9 Preference

A **Preference** represents a preferential treatment available under an applicable trade arrangement.

Examples:

- preferential tariff
- tariff elimination
- tariff reduction
- quota preference.

Preference should be modeled separately from Agreement because the existence of an agreement does not itself prove that a specific preference applies.

### 3.10 Tariff

A **Tariff** represents a tariff condition applicable to a product in a specified trade regime and period.

It may include:

- HS code
- importing jurisdiction
- tariff rate
- tariff type
- preferential/non-preferential status
- quota relationship
- effective period
- source dataset
- methodology.

Tariff calculations should remain deterministic where the underlying inputs are deterministic.

### 3.11 Non-Tariff Measure

A **Non-Tariff Measure (NTM)** represents a measure affecting international trade other than a conventional tariff.

Examples may include:

- sanitary and phytosanitary measures
- technical barriers to trade
- licensing
- quotas
- inspection requirements
- labelling rules
- registration requirements.

NTMs should preserve their classification and source rather than being treated as free-text restrictions.

### 3.12 Export Scenario

An **Export Scenario** is the concrete context for analysing a potential export.

Minimum conceptual inputs:

```text
Product
+ Origin
+ Destination
+ Date
+ HS classification
```

Additional context may include:

- exporter type
- processing state
- quantity
- value
- intended market
- certificate status
- origin status
- agreement eligibility facts.

The Export Scenario is the central object for use-case workflows such as requirements, compliance, market access and opportunity analysis.

### 3.13 Source

A **Source** identifies the authoritative or upstream origin from which information was obtained.

Examples:

- Nigerian government agency
- WTO
- ITC
- UN Comtrade
- treaty repository
- official publication portal
- official API.

A Source is not necessarily the document itself.

It should capture:

- source authority
- source type
- canonical location
- trust/authority metadata
- retrieval method
- retrieval date
- update characteristics.

### 3.14 Document

A **Document** is a specific information artifact obtained from a Source.

Examples:

- PDF gazette
- regulation
- treaty text
- circular
- official webpage
- scanned publication.

A document should retain:

- source
- title
- document identifier
- publication date
- language
- version
- checksum/integrity information where appropriate
- acquisition date
- processing status
- OCR status where relevant.

A Document may contain one or more Regulatory Instruments, but these concepts should not be assumed to be identical.

### 3.15 Dataset

A **Dataset** is a structured collection of trade or regulatory data obtained from a source.

Examples:

- WTO tariff dataset
- ITC trade statistics
- UN Comtrade dataset.

Dataset metadata should include:

- provider
- dataset name
- version
- coverage
- methodology
- units
- classification
- update frequency
- retrieval date.

### 3.16 Data Record

A **Data Record** is an individual structured observation within a Dataset.

For trade data, useful dimensions include:

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
- data quality/status.

A zero, missing value, estimated value and unavailable observation must not be silently treated as equivalent.

---

## 4. Evidence and Derived Knowledge

### 4.1 Assertion

An **Assertion** is a structured statement the system believes to be supported by evidence.

Examples:

- "A phytosanitary certificate is required for product X under condition Y."
- "The tariff rate for HS code X in market Y during period Z is N%."

An assertion should have:

- subject
- predicate
- object/value
- applicability context
- temporal validity
- confidence/uncertainty state
- supporting evidence.

### 4.2 Evidence Record

An **Evidence Record** identifies the specific source material supporting an assertion.

It may point to:

- document
- page
- section
- provision
- table
- dataset
- data record
- API response snapshot where appropriate.

Evidence should answer:

> "Where exactly did this claim come from?"

### 4.3 Finding

A **Finding** is an analytical conclusion produced from one or more assertions/evidence records.

Examples:

- requirements applicable to a scenario
- market-access condition
- identified opportunity
- detected regulatory change.

Findings must remain distinguishable from raw source facts.

---

## 5. Uncertainty Model

Uncertainty should be explicit rather than hidden.

Candidate states:

| State | Meaning |
|---|---|
| Confirmed | Directly supported by authoritative evidence |
| Derived | Deterministically derived from supported facts |
| Inferred | Interpretation requiring some reasoning |
| Probable | Evidence supports the conclusion but material uncertainty remains |
| Incomplete | Required information is missing |
| Conflicting | Relevant authoritative or high-quality sources disagree |
| Stale | Information may no longer represent the current state |
| Requires Verification | Human/source confirmation is necessary |

These are **evidence states**, not arbitrary AI confidence scores.

The platform should avoid presenting a numerical confidence score unless a defined methodology makes that score meaningful.

---

## 6. Temporal Model

Time is a first-class domain dimension.

The system should distinguish:

- publication date
- effective-from
- effective-to
- amendment date
- repeal date
- supersession date
- retrieval date
- dataset observation period.

A document retrieved today may describe a legal state that applied in an earlier period.

Therefore:

```text
Retrieved Today
    ≠
Effective Today
```

Queries must be capable of asking both:

- "What applies now?"
- "What applied on date X?"

---

## 7. Relationship Model

Key conceptual relationships include:

```text
PRODUCT
 ├── classified_as ──> HS_CODE
 └── subject_to ──> REQUIREMENT

HS_CODE
 └── has_tariff ──> TARIFF

COUNTRY
 └── participates_in ──> AGREEMENT

AGREEMENT
 ├── covers ──> PRODUCT / HS_CODE
 └── provides ──> PREFERENCE

PREFERENCE
 └── applies_under ──> APPLICABILITY CONDITIONS

REGULATORY_INSTRUMENT
 └── contains ──> PROVISION

PROVISION
 └── supports ──> ASSERTION

ASSERTION
 └── supported_by ──> EVIDENCE_RECORD

EVIDENCE_RECORD
 ├── references ──> DOCUMENT
 ├── references ──> PROVISION
 └── references ──> DATA_RECORD

DOCUMENT
 └── obtained_from ──> SOURCE

DATASET
 └── contains ──> DATA_RECORD

EXPORT_SCENARIO
 ├── concerns ──> PRODUCT
 ├── originates_in ──> COUNTRY
 ├── targets ──> MARKET / JURISDICTION
 └── evaluated_at ──> TIME

REQUIREMENT
 ├── derived_from ──> PROVISION
 └── administered_by ──> AGENCY
```

---

## 8. Knowledge Graph vs Application Data

Not every object needs to live in the knowledge graph.

### Strong candidates for the Knowledge Graph

These benefit from relationship-centric modelling:

- Product
- HS Code
- Country
- Market/Jurisdiction
- Regulatory Instrument
- Provision
- Requirement
- Agreement
- Preference
- NTM
- Agency
- Source
- temporal relationships
- amendment/supersession relationships
- applicability relationships
- provenance relationships.

### Strong candidates for Relational/Application Storage

These are primarily transactional or operational:

- User
- Role
- Permission
- Export Scenario
- saved research
- alert subscription
- workflow/task
- ingestion job
- processing job
- audit event
- API credential/configuration metadata
- UI preferences.

### Hybrid Candidates

Some objects may have both graph and relational representations:

- Document
- Dataset
- Data Record
- Assertion
- Evidence Record
- Finding.

The authoritative representation should be defined per object rather than duplicating data without a clear purpose.

---

## 9. Product Classification Is a Reasoning Problem

The platform should not assume:

```text
Product name → one guaranteed HS code
```

Instead:

```text
Product description
+ attributes
+ processing state
+ intended use
+ jurisdiction
+ classification version
        ↓
Candidate classifications
        ↓
Evidence / classification rules
        ↓
Confirmed or unresolved classification
```

Where classification cannot be determined reliably, the platform should expose uncertainty rather than silently selecting a code.

---

## 10. Requirement Applicability

A Requirement is not universally applicable merely because it exists.

Conceptually:

```text
Requirement
   +
Product
   +
Origin
   +
Destination
   +
Date
   +
Other Conditions
        ↓
Applicability Evaluation
        ↓
Applicable / Not Applicable / Unresolved
```

This evaluation belongs primarily to deterministic domain logic when its conditions are explicitly modelled.

AI may assist in extracting or interpreting the conditions.

---

## 11. Agreement Applicability

The system should separate:

1. agreement existence
2. agreement participation
3. product coverage
4. origin eligibility
5. destination eligibility
6. rules of origin
7. preference availability
8. preference rate
9. documentary/evidentiary conditions.

Therefore:

```text
Agreement
   ↓
Eligibility Conditions
   ↓
Scenario Evaluation
   ↓
Preference Applicability
```

---

## 12. Source Hierarchy and Conflicts

Sources may differ in authority.

The system should model source authority rather than assuming every retrieved page has equal status.

Where conflicting information exists:

- preserve both relevant records
- identify source authority
- identify dates
- identify instrument status
- determine whether one source supersedes another where evidence permits
- surface unresolved conflicts.

The system must not silently overwrite historical knowledge merely because newer information was ingested.

---

## 13. Entity Identity

Every important domain entity should have a stable internal identifier.

External identifiers should be stored separately.

Example:

```text
Internal ID: product:...
External ID: HS-2022:0901.11
Source ID: ...
```

This prevents external identifiers from becoming the only identity mechanism and allows mappings across sources and classification versions.

---

## 14. Minimal Export Analysis Object

The minimum object graph for the platform's principal workflow is:

```text
EXPORT SCENARIO
 │
 ├── PRODUCT
 │     └── HS CODE
 │
 ├── ORIGIN COUNTRY
 │
 ├── DESTINATION MARKET
 │
 ├── DATE
 │
 ├── REQUIREMENTS
 │      └── PROVISIONS
 │             └── DOCUMENTS / SOURCES
 │
 ├── MARKET ACCESS
 │      ├── TARIFF
 │      ├── PREFERENCE
 │      └── NTM
 │
 ├── AGREEMENTS
 │
 └── TRADE DATA
        └── DATA RECORDS
```

This object graph is the foundation for the principal user journey defined in Pass 1 and Pass 2.

---

## 15. Design Decisions Established by This Pass

1. **Product and HS Code are distinct concepts.**
2. **HS classifications are versioned.**
3. **Country and Market/Jurisdiction are distinct concepts.**
4. **Regulatory instruments retain their legal/institutional type.**
5. **Provisions are traceable units of authoritative content.**
6. **Requirements are derived and context-dependent.**
7. **Agreements do not automatically imply preferences.**
8. **Preference applicability must be evaluated separately.**
9. **Sources are distinct from Documents.**
10. **Datasets are distinct from individual Data Records.**
11. **Assertions and Findings are distinct from source facts.**
12. **Evidence must support important claims.**
13. **Time is a first-class dimension.**
14. **Uncertainty must be explicit.**
15. **Knowledge-graph and relational responsibilities should be separated deliberately.**
16. **AI should assist interpretation rather than silently become the authoritative domain model.**

---

## 16. Questions Carried Forward

The next design passes should determine:

- exact attributes for each entity
- identifiers and keys
- cardinalities
- graph ontology
- relational schema
- document/provision extraction model
- source authority model
- classification-version model
- temporal validity implementation
- requirement rule model
- agreement rule model
- trade-data dimensional model
- evidence representation
- AI/RAG retrieval objects.

These should be specified before implementation technology is locked in.
