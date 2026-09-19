# Knowledge Graph Ontology & Relationship Model

## 1. Purpose

This document defines the logical ontology for the NG Trade Intelligence Platform.

It describes graph node classes, relationship classes, relationship properties, temporal modelling, applicability, provenance, regulatory relationships, product/classification relationships, agreement/preference relationships, trade-data boundaries, and explicit versus inferred relationships.

The ontology is technology-neutral.

It is designed to support deterministic domain logic, semantic search, RAG and GraphRAG without making the graph itself the sole system of record.

## 2. Ontology Principles

### 2.1 Model Meaning, Not Screens

The ontology represents domain concepts rather than UI pages.

A dashboard, search page or compliance form is not an ontology entity merely because it exists in the application.

### 2.2 Relationships Are First-Class Knowledge

For this platform, knowing that two entities are related is often more valuable than knowing their isolated attributes.

Example:

~~~text
Product
  ↓ classified_as
HS Code
  ↓ subject_to
Requirement
  ↓ derived_from
Provision
  ↓ contained_in
Regulatory Instrument
  ↓ issued_by
Agency
~~~

### 2.3 Relationship Types Must Be Explicit

Avoid generic relationships such as RELATED_TO when a more meaningful relationship can be represented.

Prefer:

- applies_to
- applies_in
- derived_from
- amends
- supersedes
- covers
- provides
- administered_by
- classified_as.

### 2.4 Assertions Are Different From Relationships

A graph edge can represent a known domain relationship.

An Assertion represents a proposition whose truth is supported by evidence.

For example:

~~~text
Requirement ──derived_from──> Provision
~~~

is a domain relationship.

But:

~~~text
Requirement X applies to Product Y in Market Z
~~~

may be represented as an assertion because its applicability depends on conditions and time.

## 3. Core Node Classes

### 3.1 Reference / Domain Nodes

- Product
- HS Version
- HS Code
- Country
- Market/Jurisdiction
- Agency
- Agreement
- Preference
- Requirement
- NTM
- Tariff.

### 3.2 Regulatory Knowledge Nodes

- Regulatory Instrument
- Provision
- Regulatory Topic
- Certificate/Document Type
- Procedure
- Condition.

### 3.3 Evidence Nodes

- Source
- Document
- Dataset
- Data Record
- Evidence Record
- Assertion.

### 3.4 Analytical Nodes

- Finding
- Opportunity
- Market Assessment
- Compliance Assessment.

Some analytical objects may remain application-level objects rather than permanent graph nodes.

## 4. Core Relationship Vocabulary

| Relationship | Meaning |
|---|---|
| classified_as | Product has a classification |
| maps_to | Classification maps across versions |
| parent_of | Hierarchical classification relationship |
| applies_to | Rule/requirement applies to entity |
| applies_in | Rule applies within jurisdiction/market |
| administered_by | Agency administers measure |
| issued_by | Authority issued instrument |
| contains | Parent contains child |
| contained_in | Child belongs to parent |
| supports | Evidence supports assertion |
| derived_from | Knowledge derived from source/provision |
| references | One information object references another |
| amends | Instrument modifies another instrument |
| supersedes | Instrument replaces another |
| repeals | Instrument repeals another |
| implements | Instrument implements another instrument/agreement |
| participates_in | Country/party participates in agreement |
| covers | Agreement/measure covers product or market |
| provides | Agreement provides preference |
| eligible_under | Entity may qualify under a rule |
| subject_to | Product/scenario is subject to measure |
| requires | Scenario/product requires document or action |
| traded_with | Reporter trades with partner |
| reported_by | Record is reported by entity |
| measured_by | Finding/indicator uses measure |
| targets | Scenario/measure targets market |
| originates_in | Product/scenario originates in jurisdiction |
| valid_during | Relationship is valid during period |

Relationship names should use a controlled vocabulary.

## 5. Regulatory Graph

The regulatory graph is the central legal-knowledge structure.

~~~text
AGENCY
  ↑ issued_by
REGULATORY INSTRUMENT
  │
  ├── contains ──> PROVISION
  │                  │
  │                  ├── supports ──> REQUIREMENT
  │                  │                    │
  │                  │                    ├── applies_to ──> PRODUCT
  │                  │                    ├── applies_to ──> HS CODE
  │                  │                    ├── applies_in ──> MARKET
  │                  │                    └── administered_by ──> AGENCY
  │                  │
  │                  └── references ──> PROVISION / INSTRUMENT
  │
  ├── amends ──> REGULATORY INSTRUMENT
  ├── supersedes ──> REGULATORY INSTRUMENT
  └── implements ──> AGREEMENT
~~~

This allows the system to traverse from a user-facing requirement back to the exact regulatory basis.

## 6. Product and Classification Graph

The classification graph should preserve both product semantics and formal classification.

~~~text
PRODUCT
  │
  ├── classified_as ──> HS CODE
  │                       │
  │                       ├── parent_of ──> HS CODE
  │                       └── maps_to ──> HS CODE (other version)
  │
  └── has_attribute ──> PRODUCT ATTRIBUTE
~~~

A product-to-HS relationship may have properties such as:

- classification status
- classification basis
- classification source
- valid-from
- valid-to
- evidence state.

Potential classification states:

- candidate
- suggested
- confirmed
- disputed
- unresolved.

The system should not silently convert an AI-suggested classification into a confirmed classification.

## 7. Agreement and Preference Graph

~~~text
COUNTRY
   │
   └── participates_in ──> AGREEMENT
                              │
                              ├── covers ──> HS CODE / PRODUCT
                              │
                              ├── contains ──> RULE OF ORIGIN
                              │
                              └── provides ──> PREFERENCE
                                                   │
                                                   ├── applies_to ──> HS CODE
                                                   ├── applies_in ──> MARKET
                                                   └── requires ──> ELIGIBILITY CONDITION
~~~

The graph must distinguish:

~~~text
Participation
    ↓
Agreement Coverage
    ↓
Product Eligibility
    ↓
Origin Eligibility
    ↓
Preference Availability
    ↓
Scenario Applicability
~~~

This prevents the common logical error:

~~~text
Nigeria has Agreement X
       ↓
Therefore Product Y gets Preference Z
~~~

The latter does not necessarily follow.

## 8. Applicability Model

Applicability is one of the most important concepts in the platform.

A simple relationship such as:

~~~text
Requirement ──applies_to──> Product
~~~

may be insufficient.

Actual applicability may depend on:

- product
- HS code
- origin
- destination
- market
- date
- processing state
- quantity
- value
- exporter type
- intended use
- agreement status
- origin criteria.

Therefore the platform should support an Applicability Assertion.

Conceptually:

~~~text
APPLICABILITY ASSERTION
 ├── subject → Requirement
 ├── product → Product / HS Code
 ├── origin → Country
 ├── destination → Market
 ├── valid period → Time
 ├── conditions → Conditions
 ├── result → Applicable / Not Applicable / Unresolved
 └── evidence → Evidence Records
~~~

This object can be evaluated by deterministic business logic.

AI may assist in identifying or interpreting conditions, but should not silently replace the applicability evaluator.

## 9. Temporal Graph

Time should apply not only to nodes but also to relationships.

Example:

~~~text
Requirement
   │
   └── applies_to ──> HS Code
          valid_from = 2026-01-01
          valid_to   = 2026-12-31
~~~

Another example:

~~~text
Instrument A
   │
   └── supersedes ──> Instrument B
          effective_from = 2026-03-01
~~~

The graph therefore needs temporal relationship properties where required.

The platform should support at least:

- valid_from
- valid_to
- effective_from
- effective_to
- asserted_at
- retrieved_at.

These dates have different meanings and must not be conflated.

## 10. Amendment and Supersession Graph

Legal history should be represented explicitly.

Example:

~~~text
Instrument A
   │
   ├── amends ──> Instrument B
   │
   └── contains ──> Provision A1

Instrument B
   └── contains ──> Provision B1
~~~

For replacement:

~~~text
Instrument C
   └── supersedes ──> Instrument B
~~~

The system should preserve historical instruments instead of deleting them when they cease to apply.

This allows questions such as:

- What applies now?
- What applied in 2024?
- What changed?
- Which provision caused the change?
- What replaced the previous requirement?

## 11. Provenance Graph

Provenance should be modelled as a traceable graph.

~~~text
FINDING
   ↓ supported_by
ASSERTION
   ↓ supported_by
EVIDENCE RECORD
   ↓ points_to
PROVISION
   ↓ contained_in
DOCUMENT
   ↓ obtained_from
SOURCE
~~~

For trade data:

~~~text
FINDING
   ↓
ASSERTION
   ↓
EVIDENCE RECORD
   ↓
DATA RECORD
   ↓
DATASET
   ↓
SOURCE
~~~

This enables evidence-aware answers and auditability.

## 12. Source Authority Model

Sources should have an authority classification.

Possible conceptual levels:

- Primary authoritative source
- Official secondary source
- International authoritative source
- Institutional source
- Curated reference source
- Analytical source
- Unverified/unknown.

Authority level is metadata, not a universal legal ranking.

The system should also retain:

- issuing authority
- publication status
- retrieval date
- source jurisdiction
- source type.

A source's authority should be evaluated in context.

## 13. Data Graph Boundary

Not all trade data should necessarily become individual graph nodes.

A useful boundary is:

~~~text
Graph
 ├── Dataset
 ├── Trade dimensions/entities
 ├── Important derived indicators
 └── Selected Data Records where relationship reasoning is valuable

Relational / Analytical Store
 └── High-volume observations
~~~

For example, millions of trade observations may be better handled by an analytical data store than represented as millions of graph nodes.

The graph can instead represent important semantic relationships while detailed observations remain in the analytical data layer.

This boundary remains an architectural decision to validate later.

## 14. Explicit vs Inferred Relationships

Relationships should have a provenance/status dimension.

Candidate states:

- Explicit
- Extracted
- Deterministically derived
- Inferred
- Proposed
- Human verified
- Rejected.

If an amendment relationship is explicitly stated in an official document, the relationship is Explicit.

If extracted by NLP from a document, it may initially be Extracted and require validation.

If generated by reasoning from several facts, it should not be presented as though it were explicitly stated.

## 15. Graph Confidence vs Evidence State

The graph should avoid a single generic confidence field.

Instead distinguish:

### Evidence state

How strongly the proposition is supported.

### Relationship provenance

How the relationship was obtained.

### Verification status

Whether a human or authoritative process has reviewed it.

Example:

~~~text
Relationship:
Requirement ──applies_to──> HS Code

Evidence state: Confirmed
Provenance: Extracted from official provision
Verification: Human reviewed
Valid from: 2026-01-01
~~~

This is more meaningful than a numerical confidence value without a defined methodology.

## 16. Regulatory Topic Graph

A controlled vocabulary of topics can improve discovery and retrieval.

Examples:

- Export Licensing
- Sanitary and Phytosanitary Measures
- Labelling
- Packaging
- Food Safety
- Customs
- Standards
- Inspection
- Certification
- Rules of Origin
- Tariffs
- Quotas
- Prohibited Goods.

Conceptually:

~~~text
Instrument
   ↓ concerns
Regulatory Topic
   ↑ concerns
Requirement
~~~

Topics are classification aids, not substitutes for the underlying legal provisions.

## 17. Certificate and Document Requirement Graph

Requirements may refer to documents or certificates.

~~~text
Requirement
   └── requires ──> Document Type
                         │
                         └── issued_by ──> Agency
~~~

Example:

~~~text
Phytosanitary Requirement
   ↓ requires
Phytosanitary Certificate
   ↓ issued_by
Relevant Competent Authority
~~~

The actual issuing authority and legal basis must come from evidence.

## 18. Graph Traversal Patterns

The ontology should support common reasoning paths.

### 18.1 Export Requirements

~~~text
Product
 → HS Code
 → Requirement
 → Applicability Conditions
 → Market
 → Provision
 → Document
 → Source
~~~

### 18.2 Agreement Preference

~~~text
Origin Country
 → Agreement
 → Product/HS Coverage
 → Rules of Origin
 → Eligibility
 → Preference
 → Destination
 → Tariff
~~~

### 18.3 Regulatory Change

~~~text
New Instrument
 → amends/supersedes
 → Previous Instrument
 → Changed Provision
 → Requirement
 → Product/HS Scope
 → Market
 → Affected Export Scenarios
~~~

### 18.4 Market Opportunity

~~~text
Product
 → HS Code
 → Trade Data
 → Importing Market
 → Import Demand
 → Competitor Countries
 → Tariff
 → Preference
 → NTM
 → Regulatory Requirements
~~~

### 18.5 Evidence Trace

~~~text
AI Answer
 → Finding
 → Assertion
 → Evidence Record
 → Provision/Data Record
 → Document/Dataset
 → Source
~~~

## 19. GraphRAG Boundary

GraphRAG should use the ontology to improve retrieval and context construction.

Conceptually:

~~~text
User Question
      ↓
Question Interpretation
      ↓
Entity / Intent Detection
      ↓
Graph Traversal
      ↓
Relevant Nodes + Relationships
      ↓
Source Documents / Data
      ↓
Evidence Assembly
      ↓
LLM Reasoning / Synthesis
      ↓
Answer + Evidence
~~~

GraphRAG should not treat every graph relationship as equally trustworthy.

Retrieval should consider:

- source authority
- evidence state
- temporal validity
- relationship provenance
- applicability
- user context.

## 20. Deterministic vs Inferred Graph Knowledge

The platform should distinguish three broad categories.

### A. Source-stated

Directly represented by authoritative material.

Example:

~~~text
Instrument A amends Instrument B
~~~

### B. Deterministically derived

Calculated from explicit facts and rules.

Example:

~~~text
HS Code + tariff table + origin regime
       ↓
Applicable tariff calculation
~~~

### C. AI-inferred

Produced through interpretation or synthesis.

Example:

~~~text
Multiple regulatory provisions
+
market data
+
scenario context
       ↓
Potential export opportunity
~~~

The UI should distinguish these categories where material.

## 21. Ontology Boundaries

The graph should not attempt to model everything.

Keep these primarily outside the domain knowledge graph unless there is a clear reason:

- user sessions
- passwords
- UI preferences
- workflow state
- notification delivery
- internal job queues
- infrastructure metrics
- transient API requests.

These belong to application/operational architecture.

## 22. Minimum Viable Ontology

The first implementable graph does not need every possible node.

A practical initial ontology is:

~~~text
Product
HS Code
Country
Market
Agency
Regulatory Instrument
Provision
Requirement
Agreement
Preference
Tariff
NTM
Source
Document
Dataset
Evidence Record
Assertion
~~~

with these essential relationships:

~~~text
classified_as
applies_to
applies_in
contains
issued_by
administered_by
derived_from
supports
references
amends
supersedes
participates_in
covers
provides
requires
maps_to
~~~

Additional ontology classes can be introduced as validated use cases require them.

## 23. Design Rules Established by This Pass

1. Relationships have explicit semantic types.
2. Applicability is contextual rather than a simple static edge.
3. Time can apply to relationships as well as entities.
4. Legal amendments and supersession are preserved as graph history.
5. Provenance is traversable from findings to sources.
6. Source authority is represented as metadata.
7. High-volume trade observations do not automatically belong as graph nodes.
8. Explicit, extracted, derived and inferred relationships are distinguishable.
9. Evidence state is distinct from generic confidence.
10. GraphRAG retrieves through domain relationships but remains evidence-aware.
11. AI inference must not be presented as source-stated fact.
12. The graph is a semantic knowledge layer, not automatically the system of record for every object.
13. The minimum ontology should remain deliberately small until real data and use cases justify expansion.

## 24. Next Pass

The next pass should define the logical persistence model:

### Pass 6 — Relational Data Model & Knowledge Storage Boundary

It should determine:

- relational tables/entities
- primary and foreign keys
- normalization boundaries
- temporal tables
- provenance tables
- document storage metadata
- trade-data fact/dimension model
- graph projection requirements
- search index requirements
- cache/read-model boundaries
- transaction boundaries
- which data is authoritative in each store.

Only after this should we make a serious technology-selection decision for databases, graph storage, search, object storage and analytics.
