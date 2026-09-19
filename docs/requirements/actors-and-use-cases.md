# Pass 2 — Actors & Use Cases

## Purpose

This pass defines who interacts with the NG Trade Intelligence Platform, what they need to accomplish, and the major workflows the system must support.

The actor model is intentionally broader than a simple "user vs administrator" model because the platform serves different information needs and may eventually operate across government, institutional, analytical and exporter contexts.

---

# 1. Actor Model

Actors are grouped into four broad categories:

1. External users
2. Institutional users
3. Platform administrators
4. External systems and data sources

## 1.1 External Users

### A01 — Exporter

A business or individual seeking to export goods from Nigeria.

Typical needs:

- Determine export requirements
- Understand destination-market requirements
- Check tariffs and preferences
- Research potential markets
- Understand required documentation
- Monitor relevant regulatory changes
- Ask trade-related questions in natural language.

The exporter may have limited knowledge of trade regulation, so the interface should support both guided workflows and expert search.

### A02 — Researcher

A user conducting research into trade, regulation, markets, products or countries.

Typical needs:

- Search documents
- Compare regulations
- analyse trade statistics
- trace evidence
- investigate agreements
- examine historical information
- export or save research findings.

### A03 — Trade/Market Analyst

A professional analysing trade performance and market opportunities.

Typical needs:

- Analyse product-market relationships
- Compare countries
- examine trade flows
- identify market trends
- evaluate market-access conditions
- combine regulatory and trade data
- produce analytical reports.

---

# 2. Institutional Users

### A04 — Government Trade Officer

An officer working with trade promotion, policy, market access or exporter support.

Typical needs:

- Research regulations
- Assist exporters
- analyse foreign markets
- monitor changes
- prepare evidence-backed briefings
- investigate trade agreements
- compare markets.

### A05 — Regulatory / Compliance Officer

A user responsible for understanding or assessing regulatory requirements.

Typical needs:

- Identify applicable requirements
- inspect source provisions
- assess compliance scenarios
- identify missing evidence
- investigate changes
- verify regulatory relationships.

### A06 — Policy / Trade Policy Analyst

A specialised analytical user concerned with trade policy and regulatory implications.

Typical needs:

- Analyse agreements
- examine tariff and non-tariff measures
- study policy changes
- investigate market-access effects
- analyse historical and current regulatory positions
- compare jurisdictions.

This actor may eventually overlap with the trade analyst role but is retained conceptually because the information and workflow requirements differ.

---

# 3. Platform Administration Actors

### A07 — Knowledge / Source Administrator

Responsible for the quality and lifecycle of authoritative information entering the platform.

Typical needs:

- Register sources
- configure ingestion
- review acquired documents
- validate extracted information
- manage source metadata
- manage document versions
- review source conflicts
- approve/publish knowledge.

### A08 — System Administrator

Responsible for technical operation of the platform.

Typical needs:

- Manage system configuration
- manage users and roles
- monitor system health
- inspect logs
- manage integrations
- manage operational settings
- respond to failures.

### A09 — Security Administrator

Responsible for security controls and access governance.

Typical needs:

- Manage security policies
- inspect security events
- manage privileged access
- review authentication/authorization events
- investigate security incidents
- maintain security configuration.

This may initially be combined with System Administrator but should remain a distinct responsibility boundary.

### A10 — Data Administrator / Data Steward

Responsible for structured data quality and governance.

Typical needs:

- Manage datasets
- validate data
- resolve quality issues
- manage classifications
- monitor freshness
- maintain mappings
- investigate anomalous data.

---

# 4. External System Actors

### A11 — Authoritative Data Source

Examples include government portals, international organisations, APIs, datasets and official publications.

The platform interacts with these sources through ingestion or integration mechanisms.

### A12 — Identity Provider

A future external identity system may authenticate users.

Examples may include institutional identity providers or standards-based identity services.

### A13 — External Application / API Consumer

Other authorised applications may consume platform information through APIs.

Potential examples:

- Government portals
- exporter systems
- institutional dashboards
- enterprise systems
- future integrated government platforms.

---

# 5. Actor Permission Concept

The actor model is not the same thing as the authorization model.

An actor describes **what a person/system needs to do**.

A role/permission model will later determine **exactly what they are allowed to do**.

For example:

```
Actor
  ↓
Role
  ↓
Permissions
  ↓
Resources / Actions
```

A government trade officer and a researcher may both read regulatory information while having different permissions for saved workspaces, reports, administrative functions or institutional data.

---

# 6. Core Use Cases

## UC01 — Search Trade Knowledge

**Actors:** All information users

User searches across regulatory, trade and market-access information.

Inputs may include:

- natural-language query
- product
- HS code
- country
- agreement
- regulation
- agency
- date.

Outputs:

- relevant documents
- provisions
- requirements
- datasets
- entities
- relationships
- evidence.

---

## UC02 — Ask the AI Trade Assistant

**Actors:** Information users

The user asks a natural-language question.

Example:

> What requirements should I consider when exporting cocoa from Nigeria to Germany?

The system should:

1. Interpret the question.
2. Identify relevant entities and constraints.
3. Retrieve authoritative sources.
4. Retrieve structured trade data where relevant.
5. Apply deterministic domain logic where applicable.
6. Generate an evidence-grounded response.
7. Present supporting sources and relevant uncertainty.

---

## UC03 — Analyse Export Requirements

**Actors:** Exporter, trade officer, compliance officer

The user provides:

- product
- HS code, if known
- origin
- destination
- date
- exporter context.

The system returns:

- Nigerian requirements
- destination requirements
- documentation
- permits
- certificates
- standards
- agency requirements
- relevant procedures
- evidence
- unresolved/verification items.

---

## UC04 — Determine / Confirm Product Classification

**Actors:** Exporter, trade analyst, trade officer, researcher

The user provides a product description.

The system:

1. Identifies possible classifications.
2. Retrieves relevant HS descriptions.
3. Shows candidate codes.
4. Shows classification evidence.
5. Indicates uncertainty where applicable.
6. Allows the user to confirm or continue investigating.

The system should not silently turn an ambiguous natural-language product description into an authoritative HS classification.

---

## UC05 — Analyse Market Access

**Actors:** Exporter, trade analyst, trade officer, policy analyst

The user specifies:

- product
- origin
- destination.

The system analyses:

- tariffs
- preferences
- rules of origin
- quotas where applicable
- NTMs
- SPS/TBT measures
- standards
- other market-access conditions.

---

## UC06 — Analyse Trade Market

**Actors:** Trade analyst, researcher, trade officer, exporter

The user selects a product and one or more markets.

The system presents:

- import demand
- trade values
- quantities
- growth
- market shares
- supplier countries
- Nigerian performance
- historical trends.

---

## UC07 — Compare Markets

**Actors:** Exporter, analyst, researcher, trade officer

The user compares multiple destination markets for a product.

The system can compare:

- market demand
- Nigerian exports
- tariffs
- preferences
- regulatory requirements
- NTMs
- competitors
- historical trends.

---

## UC08 — Analyse Agreement Applicability

**Actors:** Trade officer, policy analyst, compliance officer, analyst

The user specifies:

- origin
- destination
- product/HS code
- relevant date.

The system identifies potentially relevant agreements and evaluates applicable conditions.

Output should include:

- agreement
- participating jurisdictions
- product coverage
- applicable preference
- origin conditions
- effective period
- supporting provisions
- unresolved conditions.

---

## UC09 — Investigate a Regulation

**Actors:** Researcher, analyst, government officer, compliance officer

The user selects a regulatory instrument.

The system presents:

- instrument identity
- issuing authority
- jurisdiction
- publication information
- effective period
- current status
- amendments
- supersession/repeal relationships
- provisions
- affected requirements
- affected products/markets where known
- source evidence.

---

## UC10 — Compare Regulatory Instruments

**Actors:** Researcher, analyst, policy analyst, compliance officer

The user selects two or more instruments.

The system identifies:

- common subject matter
- differences
- changed provisions
- changed requirements
- effective dates
- supersession relationships.

AI may assist with explanation, but comparison should remain anchored to actual source content.

---

## UC11 — Analyse Regulatory Change

**Actors:** Trade officer, compliance officer, policy analyst, researcher

The system detects or receives a source update.

It determines:

1. What changed?
2. Which instrument/provision changed?
3. When does the change apply?
4. Which requirements changed?
5. Which products may be affected?
6. Which markets may be affected?
7. Which configured users/interests may be affected?

---

## UC12 — Perform Compliance Assessment

**Actors:** Exporter, compliance officer, trade officer

The user creates a trade scenario.

The system produces:

- applicable requirements
- evidence
- known documents
- missing information
- potential gaps
- verification requirements.

The output is an analytical assessment, not a government certification.

---

## UC13 — Investigate an Export Opportunity

**Actors:** Exporter, trade analyst, trade officer

The user specifies a product.

The system can identify candidate markets based on available:

- import demand
- Nigerian export performance
- growth
- competitor activity
- tariffs
- preferences
- market-access conditions
- regulatory requirements.

The platform should show the indicators and evidence behind any opportunity analysis.

---

## UC14 — Monitor a Product / Market

**Actors:** Exporter, analyst, trade officer, researcher

The user configures interests such as:

- product
- HS code
- country
- agreement
- regulation
- market.

The system monitors relevant changes and produces alerts according to configured criteria.

---

## UC15 — Save / Organise Research

**Actors:** Information users

The user may save:

- searches
- products
- markets
- analyses
- documents
- reports
- alerts
- research workspaces.

The exact workspace model remains a later UX/domain decision.

---

## UC16 — Generate an Analytical Report

**Actors:** Analyst, trade officer, policy analyst, researcher

The user selects a subject and parameters.

The system produces a structured report containing:

- findings
- supporting data
- regulatory context
- market-access information
- sources
- dates
- assumptions
- limitations.

Generated reports must preserve evidence references.

---

# 7. Administrative Use Cases

## UC17 — Register / Manage Source

**Actor:** Knowledge / Source Administrator

Manage:

- source identity
- authority
- endpoint
- acquisition method
- update schedule
- data/document type
- validation rules
- provenance requirements.

## UC18 — Review Ingested Material

**Actor:** Knowledge / Source Administrator

Review:

- newly acquired documents
- extraction results
- metadata
- classification
- duplicate detection
- source integrity
- processing failures.

## UC19 — Publish / Retire Knowledge

**Actor:** Knowledge / Source Administrator

Move information through controlled lifecycle states.

## UC20 — Manage Data Quality

**Actor:** Data Administrator / Data Steward

Investigate:

- missing data
- anomalous values
- classification issues
- mapping errors
- stale datasets
- duplicate records
- conflicting values.

## UC21 — Manage Users and Roles

**Actors:** System Administrator / Security Administrator

Manage:

- accounts
- roles
- permissions
- organisations
- privileged access
- authentication configuration.

## UC22 — Monitor Platform

**Actor:** System Administrator

Monitor:

- service health
- ingestion
- APIs
- queues
- storage
- search
- AI services
- integrations
- errors.

---

# 8. Core User Journeys

## Journey A — Exporter: "Can I export this?"

```
Product
   ↓
Classification
   ↓
Origin
   ↓
Destination
   ↓
Requirements
   ↓
Market Access
   ↓
Agreement / Preference
   ↓
Trade Data
   ↓
Assessment
   ↓
Evidence
```

## Journey B — Analyst: "Where should this product be sold?"

```
Product
   ↓
Trade Data
   ↓
Potential Markets
   ↓
Market Comparison
   ↓
Tariffs / Preferences
   ↓
Requirements / NTMs
   ↓
Competitors
   ↓
Opportunity Analysis
   ↓
Report
```

## Journey C — Regulator: "What changed?"

```
Source Update
   ↓
Instrument
   ↓
Changed Provision
   ↓
Changed Requirement
   ↓
Affected Product
   ↓
Affected Market
   ↓
Impact Analysis
   ↓
Alert / Report
```

## Journey D — Researcher: "What does the law say?"

```
Question
   ↓
Search
   ↓
Instrument
   ↓
Provision
   ↓
Related Instruments
   ↓
Historical Context
   ↓
Evidence
   ↓
Analysis
```

---

# 9. Cross-Cutting Use-Case Requirements

Important workflows should consistently support:

- identity of the user
- relevant date
- jurisdiction
- product/HS classification
- source provenance
- evidence
- uncertainty
- auditability
- appropriate access control.

---

# 10. AI vs Deterministic Responsibilities

The use-case model reinforces the separation between AI and deterministic system behaviour.

### AI may assist with:

- Natural-language understanding
- Query interpretation
- Document summarisation
- Cross-document synthesis
- Comparative explanation
- Entity extraction
- Retrieval strategy
- Natural-language report generation.

### Deterministic services should handle where possible:

- Date/effective-period logic
- HS version handling
- Explicit applicability rules
- Tariff calculations
- Data aggregation
- Permission checks
- Source status
- Version relationships
- Audit records
- Workflow state.

---

# 11. Use-Case Priority Classes

Priority is not a product ranking; it describes the intended development sequence.

### Foundation workflows

- UC01 Search Trade Knowledge
- UC02 AI Trade Assistant
- UC03 Export Requirement Analysis
- UC04 Product Classification
- UC05 Market Access Analysis
- UC08 Agreement Applicability
- UC18 Review Ingested Material
- UC20 Data Quality

### Intelligence workflows

- UC06 Market Analysis
- UC07 Market Comparison
- UC09 Regulation Investigation
- UC10 Regulatory Comparison
- UC11 Regulatory Change
- UC13 Export Opportunity Analysis
- UC14 Monitoring
- UC16 Analytical Reporting

### Platform administration

- UC17 Source Management
- UC19 Knowledge Lifecycle
- UC21 User/Role Management
- UC22 Platform Monitoring

The exact release allocation will be determined after domain and data architecture passes.

---

# 12. Actor-to-Capability Relationship

```
EXPORTER
 ├── Requirements
 ├── Market Access
 ├── Agreement Analysis
 ├── Market Intelligence
 ├── Opportunity Analysis
 └── AI Assistant

TRADE ANALYST
 ├── Trade Data
 ├── Market Intelligence
 ├── Market Comparison
 ├── Regulatory Research
 └── Reporting

GOVERNMENT TRADE OFFICER
 ├── Regulatory Intelligence
 ├── Export Requirements
 ├── Market Access
 ├── Trade Intelligence
 ├── Agreement Analysis
 └── Monitoring

COMPLIANCE / REGULATORY OFFICER
 ├── Requirements
 ├── Compliance
 ├── Regulatory Investigation
 ├── Change Intelligence
 └── Evidence

RESEARCHER
 ├── Search
 ├── Regulatory Research
 ├── Trade Data
 ├── Comparison
 └── Reporting

SOURCE ADMINISTRATOR
 ├── Source Management
 ├── Ingestion
 ├── Knowledge Lifecycle
 └── Provenance

DATA STEWARD
 ├── Dataset Management
 ├── Classification
 ├── Data Quality
 └── Validation

SYSTEM / SECURITY ADMIN
 ├── Identity
 ├── Authorization
 ├── Configuration
 ├── Monitoring
 └── Audit
```

---

# 13. Important Design Observation

The platform should not be designed as a collection of unrelated menus.

The primary UX should be **question and scenario driven**.

A user should be able to begin with:

> "I want to export X to Y."

or:

> "What changed?"

or:

> "Which markets are relevant for X?"

or:

> "What does this regulation require?"

and the system should dynamically assemble the appropriate capabilities behind the scenes.

This suggests that the eventual UI should contain both:

- **structured tools/workspaces**, and
- **natural-language intelligence**.

The AI assistant should therefore complement—not replace—the structured application.

---

# 14. Open Questions for Pass 3

The next domain-model pass should resolve:

- What exactly constitutes a Product?
- How is a Product related to an HS Code?
- How are countries and markets represented?
- What constitutes a Requirement?
- How are legal provisions represented?
- How do provisions create or modify requirements?
- How are agreements represented?
- How are tariffs represented over time?
- How are NTMs represented?
- What is an Export Scenario?
- What is a Compliance Assessment?
- What is an Evidence Record?
- What is a Source versus a Document?
- What is a Data Set versus a Data Record?
- How should uncertainty be represented?
- Which entities belong in the knowledge graph versus relational application data?

These questions form the bridge into **Pass 3 — Domain Model**.

---

## Status

**Pass:** 2 — Actors & Use Cases

**Status:** Initial actor and use-case model completed; subject to refinement during domain modelling.
