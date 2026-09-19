# NG Trade Intelligence Platform

AI-powered platform for Nigerian trade regulations, agreements, market access, and international trade intelligence.

## Purpose

The platform is intended to bring together Nigerian trade and export regulatory information with international trade rules, market-access requirements, and trade data.

The long-term system will combine:

- Nigerian laws, regulations, guidelines, procedures, standards, circulars, and related instruments
- Treaties, agreements, protocols, MOUs, and other international/regional trade instruments
- Trade and market data from sources such as WTO, ITC, UN Comtrade, and official datasets
- A regulatory knowledge graph
- Retrieval-Augmented Generation (RAG) and GraphRAG
- Deterministic business/domain logic for trade and compliance rules
- AI-assisted analysis, search, explanation, and intelligence

## Core principle

**The AI is not the source of truth.**

Authoritative source documents and structured data remain separately stored, versioned, traceable, and auditable. AI services use those sources to produce evidence-grounded results.

## Current status

**Stage: Concept & Architecture**

We are intentionally developing the domain model, requirements, information model, data sources, and architecture before committing to implementation details.

## Repository structure

```text
docs/
├── vision/
├── requirements/
├── domain/
├── architecture/
├── business-logic/
├── knowledge-model/
└── research/

architecture/
├── uml/
├── diagrams/
└── decisions/

domain/
├── legal/
├── trade/
├── regulatory/
└── market/

data-sources/
├── nigeria/
├── wto/
├── itc/
└── other/
```

## Working approach

1. Brainstorm and define the problem domain.
2. Identify actors, use cases, entities, relationships, and rules.
3. Define authoritative information sources and ingestion processes.
4. Design the knowledge model and business logic.
5. Design the system architecture and APIs.
6. Build the platform incrementally.
7. Validate outputs against authoritative sources and real-world workflows.
