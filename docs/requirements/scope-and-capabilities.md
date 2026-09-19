# Pass 1 — System Scope & Capability Model

## Purpose

This document turns the platform concept into a more explicit scope and capability boundary. It is a specification artifact, not an implementation plan.

## 1. System Boundary

The NG Trade Intelligence Platform is a **trade intelligence and regulatory knowledge system**.

Its initial responsibility is to collect, structure, relate, analyse and present authoritative information concerning:

- Nigerian exports
- Export-related Nigerian regulation
- Destination-market access
- Trade agreements and preferences
- Tariffs and non-tariff measures
- Product requirements
- International trade flows and market indicators
- Regulatory changes.

The platform is **not initially defined as**:

- A customs clearance system
- A government licensing/permit issuance system
- A replacement for official regulatory authorities
- A legal decision-maker
- A payment system
- An ERP
- A complete exporter transaction-management platform.

It may integrate with such systems in the future.

## 2. Core System Question

The platform should ultimately be able to answer or analyse:

> **Given a product, its origin, a destination market, a relevant time period and other applicable context, what regulatory, market-access and trade-intelligence information is relevant, what evidence supports it, and what does the available data indicate?**

This question is the central organising principle for the initial platform.

## 3. Scope Dimensions

The system scope has several dimensions.

### 3.1 Geographic scope

Initial:

- Nigeria as the exporting country
- Destination countries and markets relevant to Nigerian trade.

The system should be capable of expanding to additional jurisdictions without redesigning the conceptual model.

### 3.2 Trade direction

Initial:

- Exports from Nigeria.

Future:

- Imports into Nigeria
- Transit and other trade flows where useful.

### 3.3 Product scope

The platform should be designed around internationally recognised product classification, particularly HS codes.

Initial product coverage should not be hard-coded to a small commodity list. A controlled initial dataset may be used for validation, but the domain model should support broad product coverage.

### 3.4 Time scope

The system must be time-aware.

A requirement, tariff, agreement or regulation may have:

- publication date
- effective date
- expiry/end date
- amendment date
- supersession date
- retrieval date.

A result should therefore be capable of answering not only **what applies**, but **what applied at a particular point in time**.

### 3.5 Information scope

The system combines four major information domains:

1. Regulatory/legal information
2. Market-access information
3. Trade/economic data
4. Analytical intelligence.

## 4. Capability Model

Capabilities describe what the platform must be able to do. They are deliberately separated from implementation technologies.

### C01 — Source & Corpus Management

The platform shall support:

- Registration of authoritative sources
- Source authority classification
- Source metadata
- Document acquisition
- Dataset acquisition
- Source version tracking
- Retrieval-date tracking
- Source status
- Provenance
- Source validation
- Ingestion monitoring.

### C02 — Regulatory Knowledge Management

The platform shall support:

- Laws
- Regulations
- Rules
- Guidelines
- Circulars
- Standards
- Procedures
- Notices
- Other relevant regulatory instruments.

It should represent:

- jurisdiction
- issuing authority
- legal/instrument type
- publication information
- effective period
- status
- amendments
- repeal
- supersession
- relationships to requirements.

### C03 — Treaty & Agreement Intelligence

The platform shall support:

- Treaties
- Trade agreements
- Regional agreements
- Bilateral arrangements
- Protocols
- Conventions
- Preferential arrangements
- Agreement participants
- Product coverage
- Origin conditions
- Effective periods
- Relevant obligations/benefits.

The system must distinguish agreements from other regulatory instruments.

### C04 — Product & Classification Intelligence

The platform shall support:

- Products
- HS classifications
- HS versions/revisions
- Product synonyms
- Product descriptions
- Relationships between products and regulatory requirements
- Relationships between products and trade data.

Classification uncertainty should be representable rather than silently converted into a definitive HS code.

### C05 — Requirement Intelligence

The platform shall identify and organise requirements such as:

- Permits
- Certificates
- Licences
- Registrations
- Inspections
- Testing
- Standards
- Labelling
- Packaging
- Documentation
- SPS requirements
- TBT requirements
- Customs requirements
- Agency procedures.

Each requirement should be traceable to its source evidence.

### C06 — Market Access Intelligence

The platform shall support analysis of:

- Destination-market requirements
- Tariffs
- Preferences
- Rules of origin
- Quotas where applicable
- Non-tariff measures
- SPS measures
- TBT measures
- Standards
- Market-access restrictions and conditions.

### C07 — Trade Data Intelligence

The platform shall ingest and analyse structured data such as:

- Import values
- Export values
- Trade quantities
- Trade partners
- Product-level flows
- Time series
- Market shares
- Growth indicators
- Other relevant economic/trade indicators.

The system should preserve the source, unit, period, classification and methodology associated with each dataset.

### C08 — Regulatory & Trade Search

Users should be able to search across:

- Documents
- Provisions
- Requirements
- Products
- HS codes
- Countries
- Agreements
- Tariffs
- Trade data
- Sources.

Search should support both structured and natural-language interaction.

### C09 — Export Requirement Analysis

Given a defined trade scenario, the system should assemble relevant:

- Nigerian requirements
- Destination requirements
- Product requirements
- Agency requirements
- Documentation
- Certificates
- Permits
- Procedures
- Relevant agreements.

The result should distinguish confirmed requirements from information requiring further verification.

### C10 — Agreement Applicability Analysis

The platform should analyse whether an agreement or preference may be relevant based on:

- Countries/jurisdictions
- Product/HS coverage
- Origin
- Effective dates
- Agreement conditions
- Other applicability rules.

This capability should expose the underlying evidence and conditions.

### C11 — Tariff & Market Access Analysis

The system should support:

- Applicable tariff identification
- Preferential tariff analysis
- Tariff comparisons across markets
- Historical tariff analysis where data permits
- Non-tariff measure analysis
- Market-access condition comparison.

### C12 — Market Intelligence

The platform should support analysis of:

- Market demand
- Import trends
- Nigerian export performance
- Competitor suppliers
- Product-market relationships
- Market growth
- Trade concentration
- Market diversification.

### C13 — Opportunity Intelligence

The system may derive analytical indicators from:

- Market demand
- Nigerian export performance
- Competitor performance
- Tariffs
- Market-access barriers
- Regulatory requirements
- Growth trends.

Opportunity outputs must be presented as analytical findings or indicators, not as unsupported certainty.

### C14 — Compliance Assessment

The platform should support scenario-based compliance analysis.

A scenario may contain:

- Exporter context
- Product
- HS code
- Origin
- Destination
- Intended shipment
- Date
- Known certifications/documents.

The system can then produce:

- Requirements
- Evidence
- Missing information
- Potential compliance gaps
- Verification points.

### C15 — Regulatory Change Intelligence

The platform should detect and represent:

- New instruments
- Amendments
- Repeals
- Replacements
- Changed requirements
- Changed tariffs
- Changed market-access conditions.

It should be able to trace potential impact through the knowledge model.

### C16 — AI Trade Assistant

The AI layer should support:

- Natural-language questions
- Regulatory explanation
- Cross-document synthesis
- Comparative analysis
- Guided queries
- Evidence-backed summaries
- Conversational exploration.

AI responses should expose supporting evidence where appropriate.

### C17 — Knowledge Graph & Relationship Intelligence

The system should represent relationships among:

- Regulations
- Provisions
- Requirements
- Products
- HS codes
- Countries
- Agencies
- Agreements
- Tariffs
- Trade measures
- Sources.

The graph should support relationship-aware retrieval and analysis.

### C18 — Evidence & Provenance

The system shall be able to answer:

- Where did this information come from?
- Which source supports it?
- Which provision or data record supports it?
- When was the source retrieved?
- What version was used?
- What was its effective period?
- Is the source current, superseded or historical?

### C19 — Alerts & Monitoring

Potential monitoring capabilities include:

- Regulatory alerts
- Product/market alerts
- Agreement changes
- Tariff changes
- Data updates
- Source failures
- Material changes affecting configured interests.

### C20 — User, Administration & Governance

The platform should support:

- User accounts
- Roles
- Permissions
- Administrative configuration
- Source administration
- Ingestion monitoring
- Audit logs
- System health
- Data-quality controls.

## 5. Capability Relationships

The capabilities are interconnected rather than independent modules.

Example:

```
SOURCE MANAGEMENT
       ↓
REGULATORY CORPUS ─────┐
       ↓               │
KNOWLEDGE GRAPH        │
       ↓               │
REQUIREMENT ENGINE ←───┘
       ↓
MARKET ACCESS ENGINE
       ↓
TRADE INTELLIGENCE
       ↓
AI / GRAPH REASONING
       ↓
USER ANSWER / ANALYSIS
```

Trade data follows a parallel path:

```
TRADE DATA SOURCES
       ↓
DATA INGESTION
       ↓
NORMALISATION
       ↓
TRADE DATA MODEL
       ↓
ANALYTICS
       ↕
PRODUCT / COUNTRY / HS KNOWLEDGE
```

## 6. What Is Core vs Supporting

### Core capabilities

The initial platform identity is centred on:

1. Regulatory knowledge
2. Requirements intelligence
3. Market-access intelligence
4. Trade data intelligence
5. Agreement intelligence
6. Evidence/provenance
7. AI-assisted intelligence.

### Supporting capabilities

These enable the core system:

- Source management
- Ingestion
- Search
- Knowledge graph
- User management
- Administration
- Monitoring
- Audit.

## 7. Initial Release Boundary

The first usable release should prove the central intelligence loop rather than attempt every capability.

A candidate first-release loop is:

```
Select Product
      ↓
Select Origin
      ↓
Select Destination
      ↓
Select / Confirm HS Code
      ↓
Retrieve Applicable Sources
      ↓
Determine Requirements
      ↓
Retrieve Market Access Conditions
      ↓
Retrieve Relevant Trade Data
      ↓
Produce Evidence-Grounded Analysis
```

The exact MVP scope remains open until the next passes define users, use cases, data availability and validation requirements.

## 8. Explicit Out-of-Scope Decisions for Initial Phase

The following are not part of the initial core:

- Issuing government permits
- Executing customs declarations
- Processing financial transactions
- Acting as a legal authority
- Automatically guaranteeing regulatory compliance
- Automatically guaranteeing commercial success
- Replacing official source systems.

Integration with these functions may be considered later.

## 9. Capability-to-Requirement Traceability

Each capability will eventually receive:

- Functional requirements
- User stories/use cases
- Inputs
- Outputs
- Business rules
- Data dependencies
- Source dependencies
- Security requirements
- Acceptance criteria.

This traceability should allow the project to move from concept → specification → architecture → implementation without losing the original intent.

## 10. Open Scope Questions

The following should be resolved in later passes:

- Who is the primary first-release user?
- Is the first release exporter-facing, government-facing, analyst-facing, or multi-role?
- How broad should the initial regulatory corpus be?
- Which countries should be included first?
- Which trade datasets are essential for the first release?
- What constitutes sufficient evidence for an answer?
- Which capabilities require deterministic rules versus AI assistance?
- What level of compliance assessment is appropriate?
- Which alerts are material enough to trigger notification?
- Which capabilities should be read-only versus workflow-oriented?

## Status

**Pass:** 1 — System Scope & Capability Model

**Status:** Initial specification completed; subject to refinement in subsequent passes.
