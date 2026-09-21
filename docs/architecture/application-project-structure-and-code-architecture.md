# Pass 14 — Application Project Structure & Code Architecture

## Purpose

This pass turns the technology direction into a concrete repository and code-organization strategy.

The goal is to establish clear boundaries between:

- executable applications
- domain logic
- application use cases
- API transport
- persistence
- infrastructure
- AI
- ingestion
- background workers
- tests.

The structure should make the architecture visible in the repository and discourage accidental coupling.

## 1. Proposed Repository Structure

Initial target:

~~~text
ng-trade-intelligence-platform/
├── apps/
│   ├── api/
│   └── web/
├── packages/
│   ├── domain/
│   ├── application/
│   ├── contracts/
│   └── shared/
├── workers/
│   ├── ingestion/
│   ├── document-processing/
│   ├── indexing/
│   └── analysis/
├── infrastructure/
│   ├── database/
│   ├── search/
│   ├── graph/
│   ├── storage/
│   ├── identity/
│   ├── ai/
│   └── external/
├── migrations/
├── tests/
├── scripts/
├── docs/
├── data-sources/
├── .github/
├── docker/
├── README.md
├── pyproject.toml
└── package.json
~~~

This is a target structure. Directories should be created as implementation actually requires them rather than creating a large collection of empty placeholders.

## 2. Architectural Dependency Direction

The intended dependency direction is:

~~~text
API
 ↓
Application
 ↓
Domain

Infrastructure → implements ports used by Application/Domain
Workers → Application
Web → API
~~~

The domain must not depend on:

- FastAPI
- React
- PostgreSQL
- Neo4j
- Redis
- provider-specific AI SDKs
- external trade APIs.

## 3. Backend Application

The API application should remain thin.

Candidate structure:

~~~text
apps/api/
├── main.py
├── routers/
├── middleware/
├── dependencies/
├── error_handlers/
└── configuration/
~~~

API responsibilities:

- request parsing
- validation
- authentication context
- authorization
- application-service invocation
- response mapping
- HTTP error translation.

The API should not contain substantive trade or regulatory rules.

## 4. Domain Package

The domain package owns business concepts and rules.

Candidate modules:

~~~text
packages/domain/
├── product/
├── classification/
├── regulation/
├── requirement/
├── agreement/
├── preference/
├── market_access/
├── trade/
├── evidence/
├── source/
├── scenario/
├── temporal/
└── shared/
~~~

A domain module may contain:

- entities
- value objects
- domain services
- rules
- domain exceptions
- repository interfaces where appropriate.

## 5. Application Package

The application layer orchestrates use cases.

~~~text
packages/application/
├── scenarios/
├── search/
├── requirements/
├── agreements/
├── market_access/
├── research/
├── assistant/
├── evidence/
├── sources/
├── ingestion/
├── reporting/
└── administration/
~~~

Examples:

- CreateExportScenario
- EvaluateExportScenario
- SearchTradeKnowledge
- AnalyseMarketAccess
- AskTradeAssistant
- RegisterSource
- StartIngestionRun
- ReviewKnowledgeCandidate
- PublishKnowledge.

Application services coordinate. They should not duplicate domain rules.

## 6. API Routers

Candidate routers:

~~~text
apps/api/routers/
├── auth.py
├── products.py
├── classification.py
├── markets.py
├── regulations.py
├── requirements.py
├── agreements.py
├── market_access.py
├── trade_data.py
├── scenarios.py
├── search.py
├── evidence.py
├── assistant.py
├── sources.py
├── ingestion.py
└── administration.py
~~~

Routers should map HTTP operations to application use cases and remain relatively small.

## 7. API Schemas

API request/response models should be separate from persistence models.

Preferred flow:

~~~text
API Request
    ↓
Application DTO
    ↓
Domain
    ↓
Application Result
    ↓
API Response
~~~

Avoid returning ORM/database objects directly from API endpoints.

This prevents database structure from silently becoming the public API contract.

## 8. Contracts Package

The contracts package can contain stable cross-layer schemas.

~~~text
packages/contracts/
├── api/
├── events/
├── jobs/
└── shared/
~~~

Potential contents:

- API contracts
- background-job payloads
- event contracts
- integration contracts.

Contracts should remain intentionally small.

## 9. Shared Package

Shared code should be tightly controlled.

Potential contents:

- identifiers
- date/time utilities
- pagination structures
- common primitives
- cross-cutting error types.

Do not turn shared/ into a dumping ground. If something belongs to a domain, keep it in that domain.

## 10. Infrastructure

Infrastructure contains technology-specific implementations.

~~~text
infrastructure/
├── database/
├── search/
├── graph/
├── storage/
├── identity/
├── ai/
├── external/
├── messaging/
└── observability/
~~~

Examples:

~~~text
infrastructure/database/postgresql/
infrastructure/graph/neo4j/
infrastructure/search/postgresql/
infrastructure/search/opensearch/
infrastructure/storage/s3/
infrastructure/ai/openai/
~~~

These implementations should satisfy interfaces/ports defined at the appropriate architectural boundary.

## 11. Persistence Boundary

Candidate PostgreSQL structure:

~~~text
infrastructure/database/postgresql/
├── connection.py
├── models/
├── repositories/
├── mappings/
└── unit_of_work.py
~~~

The domain should not import PostgreSQL-specific code.

Important distinction:

~~~text
ORM Model ≠ Domain Entity ≠ API Schema
~~~

They may resemble one another, but they have different responsibilities.

## 12. Repository Pattern

Application/domain code can depend on repository interfaces.

Example:

~~~text
RequirementRepository
        ↓
PostgresRequirementRepository
~~~

Repositories should expose domain-relevant operations.

Prefer:

~~~text
find_applicable_requirements(...)
~~~

over exposing arbitrary SQL operations to application/domain code.

## 13. Unit of Work

Transactional operations can use an explicit unit-of-work abstraction.

Example:

~~~text
PublishKnowledge
    ↓
Update instrument
Update provisions
Update evidence
Update publication state
Write audit event
    ↓
Commit
~~~

A failed publication should not leave the authoritative domain store in an invalid intermediate state.

## 14. Workers

Workers provide separate executable entry points for long-running work.

~~~text
workers/
├── ingestion/
│   └── main.py
├── document-processing/
│   └── main.py
├── indexing/
│   └── main.py
└── analysis/
    └── main.py
~~~

Workers should call application services instead of duplicating domain logic.

## 15. Ingestion

The ingestion lifecycle follows the architecture already established:

~~~text
Acquire
 ↓
Validate
 ↓
Extract
 ↓
Normalize
 ↓
Review
 ↓
Publish
~~~

Application-level orchestration can live under:

~~~text
packages/application/ingestion/
├── acquire.py
├── validate.py
├── extract.py
├── normalize.py
├── review.py
└── publish.py
~~~

Provider-specific implementations belong in infrastructure.

## 16. Source Adapters

External sources should use adapters.

~~~text
Source Adapter Interface
       │
       ├── NigeriaAdapter
       ├── WTOAdapter
       ├── ITCAdapter
       └── GenericFileAdapter
~~~

Adapters translate provider-specific formats into canonical structures.

The domain should not understand provider-specific response formats.

## 17. AI Module

AI receives its own application/infrastructure boundary.

~~~text
packages/application/assistant/
├── ask.py
├── retrieval.py
├── evidence.py
└── response_validation.py

infrastructure/ai/
├── providers/
├── embeddings/
├── prompts/
└── retrieval/
~~~

The application layer controls:

- intent
- retrieval
- evidence assembly
- model invocation
- output validation.

The provider layer controls SDK/API-specific behaviour.

## 18. AI Tools

AI tools should be explicit application capabilities.

Examples:

~~~text
search_knowledge
get_provision
get_requirement
get_trade_data
evaluate_scenario
get_evidence
~~~

The LLM should invoke controlled application tools rather than receiving database credentials or unrestricted infrastructure access.

## 19. Graph Module

Graph infrastructure should be separate from the domain.

~~~text
infrastructure/graph/
├── neo4j/
│   ├── client.py
│   ├── repositories.py
│   ├── projections.py
│   └── queries/
└── projection/
~~~

The graph remains a semantic projection of governed knowledge unless explicitly designated otherwise.

## 20. Search Module

Search should have an application-facing interface.

~~~text
packages/application/search/
├── queries.py
├── filters.py
└── results.py

infrastructure/search/
├── postgresql/
└── opensearch/
~~~

This permits search infrastructure to evolve without rewriting application use cases.

## 21. Object Storage

Documents should be accessed through a storage abstraction.

~~~text
DocumentStorage
      ↓
S3Storage
      ↓
Object Store
~~~

The domain should refer to document identifiers/references rather than storage-provider URLs.

## 22. Configuration

Configuration should be environment-aware.

Candidate categories:

~~~text
application
database
identity
storage
search
graph
AI
external APIs
observability
~~~

Secrets must come from environment/secret-management systems and must never be committed to Git.

## 23. Environment Separation

At minimum:

~~~text
development
testing
staging
production
~~~

Environments should have separate:

- credentials
- databases
- API keys
- object storage
- identity configuration
- AI configuration where appropriate.

Production data should not casually be copied into development environments.

## 24. Database Migrations

Schema changes must be version controlled.

~~~text
migrations/
├── 0001_initial_schema
├── 0002_add_sources
├── 0003_add_requirements
└── ...
~~~

Migration tooling should support ordered migrations and CI validation.

Database schema is code and should be reviewed like application code.

## 25. Test Structure

Testing should mirror architectural boundaries.

~~~text
tests/
├── unit/
│   ├── domain/
│   └── application/
├── integration/
│   ├── database/
│   ├── search/
│   ├── graph/
│   └── external/
├── api/
├── ingestion/
├── ai/
├── security/
└── e2e/
~~~

## 26. Domain Tests

Domain tests should be deterministic and should not require an LLM.

Examples:

- temporal validity
- requirement applicability
- classification states
- agreement applicability
- origin rules
- preference eligibility
- tariff selection
- conflict resolution.

Example:

~~~text
Given:
  requirement valid from 2026-01-01
  scenario date = 2025-12-31

Expected:
  NOT APPLICABLE
~~~

## 27. Application Tests

Application tests verify orchestration.

For EvaluateExportScenario:

~~~text
Load scenario
 ↓
Resolve classification/context
 ↓
Evaluate requirements
 ↓
Evaluate agreements
 ↓
Persist evaluation
 ↓
Return result
~~~

These tests verify use-case behaviour rather than duplicating every domain-rule test.

## 28. API Tests

API tests should verify:

- authentication
- authorization
- validation
- HTTP semantics
- serialization
- errors
- pagination
- idempotency.

They should not depend on internal implementation details.

## 29. AI Tests

AI testing should be treated as a distinct category.

Test:

- retrieval correctness
- evidence inclusion
- citation correctness
- authorization isolation
- hallucination resistance
- prompt-injection resistance
- deterministic-result preservation
- provider failures.

Fixed evaluation scenarios should be retained for regression testing.

## 30. Ingestion Tests

Each source adapter should have representative fixtures.

Example:

~~~text
Source fixture
 ↓
Adapter
 ↓
Canonical record
 ↓
Validation
~~~

Provider schema changes should ideally produce clear test failures instead of silently corrupting data.

## 31. Frontend Structure

The web application should also reflect domain boundaries.

Candidate structure:

~~~text
apps/web/
├── app/
├── components/
├── features/
│   ├── search/
│   ├── scenarios/
│   ├── requirements/
│   ├── markets/
│   ├── agreements/
│   ├── trade-data/
│   ├── evidence/
│   ├── assistant/
│   ├── research/
│   └── administration/
├── lib/
├── hooks/
├── styles/
└── tests/
~~~

Features should own their UI behaviour rather than creating one enormous global component hierarchy.

## 32. Frontend API Boundary

The frontend communicates through typed API clients.

~~~text
React Feature
    ↓
API Client
    ↓
HTTP API
~~~

The frontend must not:

- connect directly to PostgreSQL
- connect directly to Neo4j
- call trade-provider APIs directly
- contain secret API keys
- implement authoritative applicability logic.

## 33. Shared Frontend Types

Where useful:

~~~text
OpenAPI
   ↓
Typed API Client / Types
   ↓
React
~~~

This reduces backend/frontend contract drift.

## 34. Local Development

The project should eventually support a reproducible local environment.

Candidate local services:

~~~text
Web
API
PostgreSQL
Worker
Object Storage
Redis (if required)
~~~

Neo4j and OpenSearch should initially be optional development profiles if possible.

## 35. Developer Workflow

Initial workflow:

~~~text
Create branch
 ↓
Implement small change
 ↓
Format / lint
 ↓
Run tests
 ↓
Commit
 ↓
Pull request
 ↓
CI
 ↓
Review
 ↓
Merge
~~~

Documentation and ADRs should evolve alongside implementation.

## 36. Code Quality Gates

CI should eventually check:

- formatting
- linting
- type checking
- unit tests
- integration tests
- migration validity
- dependency vulnerabilities
- secret scanning
- API contract validation
- frontend tests
- accessibility checks where applicable.

## 37. Logging and Observability

Application code should use structured logging.

Useful context includes:

- request ID
- correlation ID
- job ID
- source ID
- ingestion run ID
- scenario ID.

Sensitive data must be excluded or redacted.

Instrumentation should work consistently across API, workers, ingestion, adapters and AI calls.

## 38. Feature Development Pattern

A new feature should generally follow:

~~~text
1. Domain requirement
2. Domain model/rule
3. Application use case
4. Repository/port if required
5. Infrastructure implementation
6. API contract
7. UI feature
8. Tests
9. Documentation
~~~

Avoid starting with a UI and then pushing business logic downward until the feature happens to work.

## 39. First Executable Vertical Slice

The first implementation should be deliberately small but end-to-end:

~~~text
Product
   ↓
HS Code
   ↓
Origin
   ↓
Destination
   ↓
Export Scenario
   ↓
Basic Requirement Evaluation
   ↓
Evidence
   ↓
API
   ↓
Simple Web UI
~~~

This proves the architecture before the platform expands.

## 40. First Vertical Slice Scope

### Domain

- Product
- HS Code
- Country
- Market
- Requirement
- Source
- Document
- Provision
- Evidence
- Export Scenario
- Applicability Evaluation.

### Application

- create scenario
- retrieve scenario
- evaluate scenario
- retrieve evidence.

### API

~~~text
POST /api/v1/export-scenarios
POST /api/v1/export-scenarios/{id}/evaluate
GET  /api/v1/export-scenarios/{id}
GET  /api/v1/export-scenarios/{id}/results
GET  /api/v1/evidence/{id}
~~~

### UI

- scenario form
- evaluation result
- evidence panel.

## 41. Seed Data

The first implementation should use clearly labelled development/test data.

It must not pretend that manually created sample requirements are authoritative Nigerian law.

Seed records should carry explicit development/test provenance such as:

~~~text
ENVIRONMENT = DEVELOPMENT
SOURCE STATUS = SAMPLE / NON-AUTHORITATIVE
~~~

## 42. First Implementation Rules

The first executable version should prove:

1. API does not contain core domain rules.
2. Domain evaluation is deterministic.
3. Evidence is traceable.
4. Scenario inputs are persisted.
5. Evaluation results are reproducible.
6. Database access is behind a persistence boundary.
7. UI uses the API.
8. Test data is distinguishable from authoritative data.
9. AI can be added without rewriting the domain.
10. A graph projection can be added without rewriting the domain.

## 43. Repository Evolution

The repository should transition incrementally:

~~~text
Architecture
    ↓
Project Skeleton
    ↓
Development Infrastructure
    ↓
Domain Kernel
    ↓
Persistence
    ↓
Application Services
    ↓
API
    ↓
Tests
    ↓
Web UI
    ↓
First Vertical Slice
~~~

Do not create dozens of empty abstractions merely to make the repository look complete.

## 44. Initial Implementation Boundary

The beginning of coding should likely establish:

~~~text
apps/
  api/
  web/

packages/
  domain/
  application/
  contracts/

infrastructure/
  database/
  storage/

tests/

migrations/

docker/

scripts/
~~~

Additional infrastructure such as graph, search and AI can be added when their first implementation is introduced.

## 45. Architecture Invariants

1. Domain logic is framework-independent.
2. API code is transport-focused.
3. Application services orchestrate use cases.
4. Infrastructure implements technical details.
5. Persistence models are not automatically public API models.
6. Workers reuse application/domain logic.
7. AI uses controlled application tools.
8. Frontend never accesses authoritative storage directly.
9. External providers are isolated behind adapters.
10. Tests mirror architectural boundaries.
11. Configuration and secrets remain outside source code.
12. Derived infrastructure can be introduced without rewriting the domain.
13. The first implementation should prove a complete vertical slice.
14. Repository structure should evolve with actual code rather than speculative empty abstractions.

## 46. Next Pass

**Pass 15 — First Executable Foundation / Repository Bootstrap**

The next pass transitions from architecture to implementation.

It should establish:

- Python project configuration
- FastAPI application skeleton
- React/TypeScript web application skeleton
- PostgreSQL development environment
- Docker Compose
- environment configuration
- database migration framework
- initial domain package
- initial application package
- health endpoint
- basic API contract
- test framework
- linting/type checking
- CI workflow
- development README
- architecture enforcement conventions.

After Pass 15, the project can begin implementing the first vertical slice rather than adding another purely conceptual layer.
