# Pass 13 — Technology Architecture & Technology Selection

## 1. Purpose

This pass translates the logical architecture into concrete technology candidates.

The objective is not to select technology because it is fashionable or familiar. Technology must fit the domain, evidence requirements, security model, analytical workload and expected deployment environment.

The architecture established in previous passes remains authoritative over technology choices.

---

## 2. Technology Selection Principles

Technology selection should favour:

1. Correctness
2. Domain fit
3. Security
4. Maintainability
5. Interoperability
6. Developer productivity
7. Operational simplicity
8. Testability
9. Portability
10. Scalability where actually required
11. Cost sustainability
12. Institutional deployment suitability.

The platform should avoid introducing infrastructure merely because the technology is capable of doing something.

---

## 3. Proposed Initial Technology Direction

The current leading architecture is:

~~~text
Frontend
   ↓
TypeScript Web Application
   ↓
Python API / Application Layer
   ↓
Domain Services
   ↓
PostgreSQL
   ├── pgvector where appropriate
   │
   ├── Search / relational retrieval
   │
   └── Authoritative domain data
   ↓
Object Storage
   ↓
Background Workers
   ↓
External Trade / AI / Source APIs

Optional / later:
Neo4j Knowledge Graph
Dedicated Search Engine
Dedicated Analytical Engine
~~~

This is a **technology direction**, not yet an irreversible implementation lock.

---

## 4. Backend Candidate

### Leading candidate: Python

Python is a strong fit because the platform combines:

- web APIs
- data engineering
- document processing
- OCR pipelines
- AI/LLM integration
- embeddings
- graph processing
- analytical workloads
- trade-data processing.

The Python ecosystem also provides mature tooling for data and AI workflows.

### API framework candidates

Primary candidate:

**FastAPI**

Alternative:

- Django
- Flask
- other ASGI frameworks.

FastAPI is particularly attractive for an API-first system with typed request/response models and OpenAPI integration.

The final decision should consider the required authentication, dependency injection, ORM/data-access, background processing and team workflow.

---

## 5. Frontend Candidate

### Leading candidate: TypeScript + React

The web application needs:

- complex forms
- data tables
- research workspaces
- dashboards
- evidence panels
- scenario builders
- AI conversation
- document/source inspection
- administrative workflows.

React with TypeScript provides a strong component model and broad ecosystem.

A framework such as Next.js can be evaluated for:

- routing
- rendering
- application structure
- deployment
- server-side capabilities.

The frontend should not contain authoritative business rules.

---

## 6. API Contract

OpenAPI should be used as the API contract once implementation begins.

The contract should describe:

- endpoints
- request schemas
- response schemas
- errors
- authentication
- pagination
- filtering
- asynchronous jobs.

The API contract should be generated or validated against the implementation to reduce drift.

---

## 7. Relational Database

### Leading candidate: PostgreSQL

PostgreSQL fits the platform's authoritative transactional data requirements.

It is suitable for:

- users
- organizations
- permissions
- products
- HS classifications
- regulatory instruments
- provisions
- requirements
- agreements
- preferences
- sources
- evidence
- scenarios
- workflow state
- audit metadata.

It also provides mature relational integrity and indexing capabilities.

The architecture should treat PostgreSQL as the likely authoritative system of record for the core application/domain model.

---

## 8. PostgreSQL and Vector Search

PostgreSQL can potentially host vector data through pgvector.

This creates an important architectural option:

~~~text
PostgreSQL
 ├── relational domain data
 ├── full-text/search-supporting structures
 └── vector embeddings
~~~

This may be sufficient for the first implementation.

A separate vector/search platform should only be introduced when search requirements justify its operational cost.

---

## 9. Knowledge Graph Candidate

### Leading candidate: Neo4j

Neo4j is a strong candidate for the semantic knowledge graph because the project explicitly requires:

- relationship-rich regulatory knowledge
- multi-hop traversal
- provenance paths
- agreement relationships
- product/HS mappings
- regulatory relationships
- GraphRAG.

Neo4j's current GraphRAG tooling supports graph retrieval, vector retrieval and integration with multiple model providers. Its current documentation also supports in-index filtering for compatible vector searches on Neo4j 2026.01+. citeturn0search0turn0search1

However, Neo4j should not automatically become the system of record.

The proposed boundary remains:

~~~text
PostgreSQL
    ↓
Governed Domain Data
    ↓
Neo4j Projection
~~~

The graph should be rebuildable from authoritative data where practical.

---

## 10. Do We Need a Graph Database Immediately?

Not necessarily.

A staged approach is preferable.

### Stage A

Start with:

- PostgreSQL
- explicit relational relationships
- search
- domain services.

### Stage B

Introduce Neo4j when:

- graph traversal becomes central to user workflows
- ontology stabilises
- relationship queries become difficult to express efficiently in relational structures
- GraphRAG needs richer traversal
- provenance navigation becomes a major capability.

### Stage C

Use the graph as a major intelligence/retrieval layer.

This avoids building an empty graph before the domain has sufficient governed knowledge.

---

## 11. Search Architecture

Search has several distinct needs:

- exact regulatory search
- full-text search
- metadata filtering
- semantic retrieval
- hybrid retrieval
- citation/provenance lookup.

The initial architecture should avoid assuming one search technology must solve every problem.

Candidate options:

### PostgreSQL

Good for:

- exact lookup
- relational filtering
- moderate full-text search
- authoritative retrieval.

### OpenSearch

Candidate when the platform requires:

- large-scale full-text search
- advanced filtering
- hybrid search
- semantic/vector search
- search-specific scaling.

OpenSearch currently provides vector search and documents semantic and hybrid search capabilities. citeturn0search4turn0search7turn0search10

### Neo4j

Useful for:

- graph-aware retrieval
- relationship traversal
- graph-based context.

Therefore the eventual architecture may use:

~~~text
Exact / transactional → PostgreSQL
Semantic / document search → Search layer
Relationship retrieval → Neo4j
~~~

But the first release should minimise unnecessary infrastructure.

---

## 12. Object / Document Storage

A separate object store should hold source artifacts such as:

- PDFs
- scanned gazettes
- DOCX files
- spreadsheets
- XML/JSON source files
- HTML snapshots
- OCR artifacts.

The relational database should store metadata and references, not large binary documents as the default approach.

Candidate technologies include:

- S3-compatible object storage
- MinIO for self-hosted environments
- cloud object storage where appropriate.

The exact provider depends on deployment requirements.

---

## 13. Document Processing

Document processing will likely use Python-based workers.

Potential components:

- PDF text extraction
- OCR
- document structure detection
- spreadsheet parsing
- XML/JSON processing
- table extraction
- entity extraction
- provision segmentation.

The architecture should isolate processing from the API process.

---

## 14. Background Processing

Background jobs are required for:

- source acquisition
- document processing
- OCR
- knowledge extraction
- embedding generation
- search indexing
- graph projection
- trade-data ingestion
- change detection
- report generation
- notifications.

Candidate technologies:

- Celery
- RQ
- Dramatiq
- a framework-specific task system
- queue-backed workers.

Initial choice should favour operational simplicity.

A dedicated distributed event platform is not required simply because asynchronous jobs exist.

---

## 15. Queue / Broker

A message broker may eventually be useful.

Candidate:

**Redis**

Potential uses:

- job queue
- short-lived cache
- rate limiting
- distributed coordination where justified.

However, Redis should not become the authoritative store for domain knowledge.

For larger event-driven workloads, alternatives can be evaluated later.

---

## 16. Cache

Caching can improve:

- repeated reference lookups
- expensive analytical queries
- external API responses
- common search context
- frequently requested market data.

But:

~~~text
Cache ≠ Source of Truth
~~~

Every cache needs:

- freshness policy
- invalidation strategy
- failure behaviour.

Incorrectly cached regulatory information could be more dangerous than a slow query, so regulatory caching requires particular care.

---

## 17. Analytical Trade Data

Trade datasets can become substantially larger than transactional application data.

The architecture should therefore distinguish:

~~~text
Operational / Domain Data
        ↓
PostgreSQL

High-volume Trade Observations
        ↓
Analytical Storage
~~~

Potential technologies to evaluate later include:

- PostgreSQL partitioned tables
- DuckDB for local/batch analytical processing
- ClickHouse for larger analytical workloads
- cloud data warehouse solutions.

The initial implementation can begin with PostgreSQL if the expected dataset size and query volume permit it.

---

## 18. AI / LLM Integration

The AI layer should use an internal provider abstraction.

~~~text
AI Application Service
       ↓
LLM Interface
       ↓
Provider Adapter
       ├── OpenAI
       ├── Anthropic
       ├── Google
       ├── Local model
       └── Other provider
~~~

The domain/application layer should not depend directly on one provider's SDK.

This preserves portability and supports institutional deployment policies.

---

## 19. GraphRAG Technology

If Neo4j is selected, its current official Python GraphRAG package provides:

- GraphRAG
- vector retrieval
- graph retrieval
- knowledge-graph construction pipelines
- multiple LLM integrations.

It supports Python 3.10+ and current Neo4j versions including 2026.01+. citeturn0search0turn0search5

The platform should still implement its own **evidence and authorization layer** around GraphRAG rather than treating a generic GraphRAG library as the application's complete retrieval architecture.

---

## 20. AI Provider Strategy

The architecture should support three deployment modes conceptually.

### External model

~~~text
Platform → Secure API → External LLM
~~~

Useful where institutional policy permits external processing.

### Private hosted model

~~~text
Platform → Internal Model Endpoint
~~~

Useful where data must remain inside controlled infrastructure.

### Hybrid

~~~text
Public / low-risk data → External Model
Sensitive / restricted data → Approved Internal Model
~~~

The selected mode should be controlled by policy, data classification and deployment requirements.

---

## 21. Authentication Technology

Candidate standard:

- OpenID Connect
- OAuth 2.0.

Potential identity platforms:

- Microsoft Entra ID
- Keycloak
- Auth0
- another institutional identity provider.

For institutional/government deployments, the architecture should support integration with an existing organizational identity provider rather than requiring every organization to create a separate account system.

---

## 22. Containers

Containerisation is a strong candidate for development and deployment consistency.

Conceptually:

~~~text
Web
API
Worker
Scheduler
PostgreSQL
Redis
Object Storage
Neo4j (optional)
Search (optional)
~~~

Docker-compatible development can make the local environment reproducible.

Production deployment remains deployment-environment dependent.

---

## 23. Deployment Options

The architecture should remain portable across:

### Self-hosted

Useful for:

- institutional environments
- controlled government infrastructure
- restricted datasets
- private AI deployment.

### Cloud

Useful for:

- managed databases
- scalable storage
- managed identity
- managed observability
- easier horizontal scaling.

### Hybrid

Potentially useful where:

- sensitive data remains institutional
- selected services use cloud infrastructure
- external AI APIs are permitted selectively.

The application should avoid unnecessary dependence on a single cloud provider at the domain-code level.

---

## 24. Observability

The platform should eventually support:

- structured logging
- metrics
- distributed traces where useful
- job monitoring
- ingestion monitoring
- API latency monitoring
- source freshness monitoring
- AI request monitoring
- security event monitoring.

OpenTelemetry is a strong candidate for instrumentation interoperability.

---

## 25. CI/CD

The repository should evolve toward:

~~~text
Commit
  ↓
Lint
  ↓
Unit Tests
  ↓
Integration Tests
  ↓
Security Checks
  ↓
Build
  ↓
Deploy to Test
  ↓
Validation
  ↓
Production Deployment
~~~

Potential tooling:

- GitHub Actions
- container image registry
- automated dependency updates
- secret scanning
- static analysis.

The exact pipeline will be defined when implementation begins.

---

## 26. Testing Stack

Testing should reflect the architecture.

### Backend

- unit tests
- domain-rule tests
- integration tests
- API tests
- database tests.

### Frontend

- component tests
- accessibility tests
- end-to-end tests.

### Data

- ingestion tests
- schema validation
- data-quality tests
- source regression tests.

### AI

- retrieval evaluation
- citation/evidence tests
- hallucination tests
- prompt-injection tests
- regression datasets
- authorization leakage tests.

---

## 27. Development Environment

A practical initial environment could be:

~~~text
Windows / Linux / macOS
       ↓
Git
       ↓
Python
       ↓
Node.js
       ↓
Docker
       ↓
PostgreSQL
       ↓
Optional Redis
       ↓
Optional Neo4j
~~~

The project should document supported development environments once implementation starts.

---

## 28. Initial Technology Profile

The current preferred baseline is therefore:

| Area | Initial direction | Status |
|---|---|---|
| Frontend | TypeScript + React | Preferred candidate |
| Web framework | Next.js or equivalent | Evaluate |
| Backend | Python | Preferred candidate |
| API | FastAPI | Preferred candidate |
| Core DB | PostgreSQL | Preferred candidate |
| Vector | pgvector initially | Preferred candidate |
| Graph | Neo4j | Candidate / staged |
| Search | PostgreSQL initially; OpenSearch later if needed | Staged |
| Object storage | S3-compatible | Preferred pattern |
| Jobs | Redis + worker framework | Candidate |
| AI | Provider abstraction | Required |
| Identity | OIDC/OAuth 2.0 | Required |
| Containers | Docker-compatible | Preferred |
| Observability | OpenTelemetry-compatible | Preferred |
| CI/CD | GitHub Actions or equivalent | Preferred |

These are architectural candidates, not final irreversible selections.

---

## 29. Recommended Initial Deployment Shape

The first development deployment can remain intentionally small:

~~~text
┌─────────────────────────────────────────┐
│              Web Application            │
└───────────────────┬─────────────────────┘
                    │
              ┌─────▼─────┐
              │   API     │
              │  FastAPI  │
              └─────┬─────┘
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
   PostgreSQL     Redis       Object Store
        │
        └── pgvector

Background Worker
        │
        ├── ingestion
        ├── document processing
        ├── indexing
        └── analysis

Optional later:
        ├── Neo4j
        └── OpenSearch
~~~

This gives us a useful development platform without requiring every future component from day one.

---

## 30. Technology Introduction Strategy

Introduce infrastructure according to actual need.

### Start

- React/TypeScript
- Python/FastAPI
- PostgreSQL
- pgvector
- object storage
- background worker
- Docker
- CI/CD.

### Add when justified

- Redis for more demanding queue/cache needs
- Neo4j for mature graph workloads
- OpenSearch for advanced search scale/relevance
- analytical database for high-volume trade data
- dedicated event infrastructure for distributed workflows.

This keeps the initial system understandable.

---

## 31. Technology Selection Matrix

Future technology decisions should be documented against:

| Criterion | Questions |
|---|---|
| Domain fit | Does it represent the required concepts well? |
| Correctness | Can it preserve temporal/provenance requirements? |
| Security | Can access and isolation be enforced? |
| Scale | Does it handle expected workload? |
| Query model | Does it support required access patterns? |
| Integration | Does it integrate with the surrounding system? |
| Operations | How difficult is it to operate? |
| Cost | What is the total cost? |
| Portability | Can it move between environments? |
| Ecosystem | Is the ecosystem mature? |
| Team fit | Can the development team maintain it? |
| Governance | Is it suitable for institutional deployment? |

---

## 32. Technology Decision Records

Technology choices should be recorded as ADRs.

For example:

~~~text
ADR-0002 Backend Framework
ADR-0003 Frontend Architecture
ADR-0004 Primary Database
ADR-0005 Search Strategy
ADR-0006 Knowledge Graph Strategy
ADR-0007 Background Processing
ADR-0008 Identity Provider Strategy
ADR-0009 AI Provider Abstraction
~~~

An ADR should explain:

- context
- options
- evaluation criteria
- decision
- consequences
- assumptions
- reconsideration triggers.

---

## 33. Current Technology Decision Gates

Before implementation, the following decisions should be explicitly confirmed:

### Gate A — Application stack

Python + FastAPI + TypeScript/React.

### Gate B — System of record

PostgreSQL.

### Gate C — Initial semantic retrieval

PostgreSQL + pgvector, unless prototype testing shows a clear need for another solution.

### Gate D — Knowledge graph

Neo4j as a staged component rather than an immediate mandatory dependency.

### Gate E — Search

Start with PostgreSQL capabilities; evaluate OpenSearch after realistic corpus/search benchmarks.

### Gate F — Trade analytics

Begin with PostgreSQL where practical; benchmark before introducing a dedicated analytical engine.

### Gate G — AI

Provider-independent abstraction with policy-controlled model access.

---

## 34. Why This Architecture Is Deliberately Conservative

The platform is ambitious, but the first implementation should not attempt to operate:

- a relational database
- graph database
- search cluster
- vector database
- event bus
- cache cluster
- analytical warehouse
- multiple model servers

before there is actual workload requiring them.

The architecture supports these components without making them mandatory.

That distinction is important.

---

## 35. Technology Architecture Invariants

1. PostgreSQL remains the likely authoritative core store.
2. Derived stores remain rebuildable where practical.
3. Domain logic remains independent of infrastructure.
4. External providers are accessed through adapters.
5. AI providers remain replaceable.
6. The graph is introduced according to actual graph workload.
7. Search infrastructure is introduced according to measured search requirements.
8. High-volume analytical storage is introduced according to measured data volume.
9. Infrastructure complexity must have a demonstrated architectural reason.
10. Technology choices are recorded in ADRs.
11. The deployment model must not dictate the domain model.
12. Security requirements established in Pass 12 constrain technology selection.
13. The platform remains capable of institutional/self-hosted deployment.
14. No single vendor should become an invisible architectural dependency.

---

## 36. Next Pass

**Pass 14 — Application Project Structure & Code Architecture**

The next pass should turn the technology direction into an actual repository/code structure.

It will define:

- frontend structure
- backend structure
- domain modules
- application services
- API routers/controllers
- repositories
- models/schemas
- configuration
- dependency injection
- background workers
- tests
- migrations
- shared types
- AI module
- ingestion module
- infrastructure adapters
- local development environment
- how the repository should evolve from documentation into executable software.

This will be the bridge from architecture into the first real implementation.
