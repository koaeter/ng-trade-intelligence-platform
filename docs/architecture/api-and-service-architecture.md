# Pass 11 — API & Service Architecture

## 1. Purpose

This pass defines the application's service boundaries and API architecture without prematurely committing the implementation to a microservice deployment model.

The objective is to establish clean boundaries between:

- HTTP/API transport
- application orchestration
- domain rules
- persistence
- search/retrieval
- AI
- ingestion
- background processing
- administration.

The first implementation should favour a modular application architecture. Logical service boundaries should exist before physical service separation.

## 2. Architectural Principle

The preferred request flow is:

~~~text
Client
  ↓
API / Transport
  ↓
Application Service
  ↓
Domain Service / Domain Model
  ↓
Repository / Port
  ↓
Persistence or External Adapter
~~~

For AI-assisted operations:

~~~text
Client
  ↓
AI Application Service
  ↓
Question / Intent Interpretation
  ↓
Retrieval Orchestration
  ↓
Domain / Search / Graph / Data Services
  ↓
Evidence Package
  ↓
LLM
  ↓
Grounded Response
~~~

The API layer should not contain business rules.

The LLM should not directly query authoritative databases without controlled retrieval and evidence assembly.

## 3. Modular Monolith First

The platform should initially be designed as a modular application, not as a collection of independently deployed microservices.

Logical modules can include:

~~~text
Identity & Access
Source Management
Knowledge Management
Product & Classification
Requirements
Agreements & Preferences
Market Access
Trade Data
Scenario Analysis
Search
Evidence & Provenance
AI Assistant
Alerts
Reporting
Administration
Audit
~~~

These modules can initially run in one deployable application.

Physical separation can be introduced later where scale, reliability or organizational boundaries justify it.

## 4. API Boundary

The API is responsible for:

- transport
- authentication
- authorization checks
- request validation
- serialization
- response formatting
- API versioning
- rate limiting
- correlation identifiers
- error translation.

It should not be responsible for:

- determining legal applicability
- calculating business rules directly
- constructing graph queries throughout controllers
- calling an LLM directly from arbitrary endpoints
- modifying persistence objects without application/domain orchestration.

## 5. API Style

The initial platform can primarily use HTTP/JSON APIs.

Candidate principles:

- resource-oriented endpoints
- standard HTTP semantics
- JSON request/response representations
- OpenAPI documentation
- consistent error responses
- explicit API versioning
- pagination
- filtering
- sorting
- idempotency where required.

Alternative interfaces such as GraphQL or event APIs can be introduced later if justified by actual requirements.

## 6. API Versioning

The external API should have an explicit compatibility strategy.

Initial conceptual approach:

~~~text
/api/v1/...
~~~

Versioning should be introduced for meaningful contract changes, not every internal implementation change.

## 7. Core API Domains

The initial API surface can be organized around business capabilities.

### Identity

~~~text
/api/v1/users
/api/v1/roles
/api/v1/permissions
~~~

### Products / Classification

~~~text
/api/v1/products
/api/v1/hs-codes
/api/v1/classifications
~~~

### Markets

~~~text
/api/v1/countries
/api/v1/markets
~~~

### Regulatory Knowledge

~~~text
/api/v1/instruments
/api/v1/provisions
/api/v1/requirements
~~~

### Agreements

~~~text
/api/v1/agreements
/api/v1/preferences
/api/v1/rules-of-origin
~~~

### Market Access

~~~text
/api/v1/tariffs
/api/v1/ntms
/api/v1/market-access
~~~

### Trade Data

~~~text
/api/v1/trade-data
/api/v1/datasets
/api/v1/indicators
~~~

### Research

~~~text
/api/v1/search
/api/v1/research
/api/v1/reports
~~~

### Scenarios

~~~text
/api/v1/export-scenarios
/api/v1/export-scenarios/{id}/evaluate
/api/v1/export-scenarios/{id}/results
~~~

### Evidence

~~~text
/api/v1/evidence
/api/v1/sources
/api/v1/documents
~~~

### AI

~~~text
/api/v1/assistant/sessions
/api/v1/assistant/messages
~~~

### Administration / ingestion

~~~text
/api/v1/sources
/api/v1/ingestion-runs
/api/v1/review
/api/v1/quality
~~~

Exact endpoint names remain subject to later API design.

## 8. Application Service Layer

Application services orchestrate use cases.

Examples:

- CreateExportScenario
- EvaluateExportScenario
- SearchTradeKnowledge
- AnalyseMarketAccess
- AnalyseAgreementApplicability
- GenerateMarketComparison
- AskTradeAssistant
- CreateResearchReport
- RegisterSource
- StartIngestionRun
- ReviewKnowledgeCandidate
- PublishKnowledge

An application service coordinates work. It should not become a second database model or contain every domain rule.

## 9. Domain Service Layer

Domain services contain reusable business rules.

Examples:

~~~text
ClassificationService
RequirementApplicabilityService
AgreementService
OriginEligibilityService
PreferenceService
TariffService
NtmService
TemporalValidityService
EvidenceService
ConflictResolutionService
EvaluationTraceService
~~~

A domain service should be usable independently of HTTP.

## 10. Repository / Port Boundary

Application/domain code should depend on interfaces or ports rather than concrete storage implementations.

~~~text
Domain
  ↓
Repository Interface
  ↓
Implementation
  ├── PostgreSQL
  ├── Graph database
  ├── Search index
  └── External API adapter
~~~

This improves testing, portability and infrastructure replacement.

## 11. Scenario Analysis API

The export scenario is one of the central application concepts.

A scenario may contain:

- Product
- HS Code
- Origin
- Destination
- Scenario Date
- Exporter Context
- Quantity
- Value
- Processing Information
- Intended Use
- Agreement / Preference Context

Creation:

~~~http
POST /api/v1/export-scenarios
~~~

Evaluation:

~~~http
POST /api/v1/export-scenarios/{id}/evaluate
~~~

Result:

~~~http
GET /api/v1/export-scenarios/{id}/results
~~~

Evaluation should produce a durable result record where appropriate, rather than forcing the client to repeat expensive analysis.

## 12. Synchronous vs Asynchronous Evaluation

### Synchronous candidates

- simple lookup
- product lookup
- country lookup
- basic search
- small deterministic evaluation.

### Asynchronous candidates

- large trade-data analysis
- report generation
- complex GraphRAG analysis
- document ingestion
- OCR
- embedding generation
- large-scale reindexing
- regulatory impact analysis.

Conceptually:

~~~text
POST request
   ↓
Job created
   ↓
202 Accepted
   ↓
Background processing
   ↓
Result available
~~~

## 13. Job Model

Long-running work should have an explicit job model.

Candidate states:

~~~text
QUEUED
RUNNING
SUCCEEDED
FAILED
CANCELLED
RETRYING
PARTIALLY_COMPLETED
~~~

Candidate metadata:

- job_id
- job_type
- requested_by
- created_at
- started_at
- completed_at
- status
- progress
- error
- correlation_id
- result_reference.

## 14. Idempotency

Operations that may be retried must be designed carefully.

Examples:

- source ingestion
- document acquisition
- publication
- report generation
- scenario evaluation
- external API writes where applicable.

For suitable commands, clients may provide an idempotency key.

The system should prevent a retry from accidentally creating duplicate authoritative records.

## 15. Search API

Search should support multiple modes:

~~~text
Keyword
Semantic
Structured filter
Graph-assisted
Hybrid
~~~

Example:

~~~http
GET /api/v1/search?q=cocoa+export+requirements
~~~

Filters may include:

- jurisdiction
- country
- market
- HS code
- product
- instrument type
- source authority
- effective date
- status
- document type.

Search results should expose enough provenance to allow the user to reach the underlying source.

## 16. Evidence API

Evidence should be addressable as a first-class resource.

Possible operations:

~~~text
GET /evidence/{id}
GET /provisions/{id}/evidence
GET /assertions/{id}/evidence
GET /findings/{id}/evidence
~~~

The purpose is to support:

~~~text
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
~~~

## 17. AI Assistant Architecture

The AI assistant should not be a generic chatbot sitting beside the application.

It should be an application capability connected to governed retrieval.

~~~text
User Question
      ↓
Assistant API
      ↓
Intent / Entity Interpretation
      ↓
Retrieval Planner
      ↓
Search / Graph / Domain Services
      ↓
Evidence Assembly
      ↓
Context Validation
      ↓
LLM
      ↓
Response Validation
      ↓
Answer + Evidence + Uncertainty
~~~

## 18. AI Assistant Session

A session may contain:

- session_id
- user_id
- conversation metadata
- messages
- retrieved evidence references
- scenario context
- timestamps
- model metadata where appropriate.

Conversation history should not automatically be treated as authoritative facts.

The assistant should distinguish:

- user-provided context
- retrieved evidence
- system/domain facts
- AI-generated interpretation.

## 19. Retrieval Planner

The retrieval planner determines which information sources are needed.

For a question such as "What do I need to export cocoa to Germany?", it may identify:

~~~text
Product
HS code
Origin
Destination
Nigerian requirements
Germany/EU requirements
Agreements
Tariffs
NTMs
Certificates
~~~

The planner should retrieve structured domain information before asking the LLM to synthesize the response.

## 20. Evidence Package

The LLM should receive a bounded evidence package.

~~~text
Evidence Package
 ├── Scenario
 ├── Applicable rules
 ├── Requirements
 ├── Agreements
 ├── Preferences
 ├── Tariffs
 ├── NTMs
 ├── Source provisions
 ├── Trade records
 ├── Conflicts
 └── Missing information
~~~

Each evidence item should carry provenance.

## 21. AI Response Contract

The assistant should conceptually return:

~~~text
AssistantResponse
 ├── answer
 ├── findings[]
 ├── evidence[]
 ├── uncertainty[]
 ├── conflicts[]
 ├── missing_information[]
 └── suggested_next_actions[]
~~~

The UI can then present the answer and allow users to inspect supporting evidence.

## 22. Response Validation

AI output should undergo post-generation checks where appropriate.

Examples:

- cited evidence actually exists
- cited provision belongs to cited document
- source references resolve
- dates are coherent
- model did not invent evidence identifiers
- unsupported claims are flagged
- deterministic results are not contradicted without explanation.

The system should prefer refusing to assert unsupported details over fabricating a complete-looking answer.

## 23. AI and Deterministic Result Boundary

If the domain engine returns:

~~~text
Preference: UNRESOLVED
Reason: Origin criterion not established
~~~

the AI should explain that uncertainty.

It should not transform it into "Preference: AVAILABLE" merely because a likely interpretation exists.

## 24. Authentication and Authorization

Authentication establishes identity.

Authorization determines what the identity can do.

~~~text
Identity Provider
      ↓
Authenticated User
      ↓
Application Identity
      ↓
Role
      ↓
Permission
      ↓
Resource / Action
~~~

Examples:

- public researcher → search published knowledge
- analyst → create research/report
- knowledge reviewer → approve candidates
- administrator → manage sources
- security administrator → inspect security events.

## 25. Resource-Level Authorization

Authorization should be evaluated at the resource/action level.

Examples:

~~~text
Can user:
  READ published requirement?
  EDIT candidate requirement?
  APPROVE requirement?
  PUBLISH requirement?
  RETIRE requirement?
  START ingestion?
  VIEW audit event?
~~~

Do not rely solely on frontend visibility for authorization. Authorization must be enforced server-side.

## 26. Public vs Protected APIs

Some information may eventually be public:

- selected published regulatory information
- country/product reference data
- public research.

Other capabilities should require authentication:

- saved research
- reports
- personalized alerts
- administrative operations
- unpublished knowledge
- review workflows.

The exact public/private boundary should be defined during security architecture.

## 27. Error Model

The API should use a consistent error structure.

Conceptually:

~~~json
{
  "type": "validation_error",
  "code": "INVALID_SCENARIO_DATE",
  "message": "Scenario date is invalid.",
  "details": [],
  "correlation_id": "..."
}
~~~

Potential categories:

- validation_error
- authentication_error
- authorization_error
- not_found
- conflict
- rate_limited
- dependency_error
- processing_error
- unavailable
- internal_error.

Do not expose internal stack traces or infrastructure details to clients.

## 28. Domain Errors vs HTTP Errors

Domain logic should not need to know HTTP status codes.

For example:

~~~text
Domain:
PreferenceEligibilityUnresolved
        ↓
Application layer
        ↓
API representation
~~~

This keeps domain logic reusable in HTTP APIs, background jobs and future messaging consumers.

## 29. Pagination, Filtering and Sorting

Collection endpoints should support predictable pagination.

Examples:

- documents
- provisions
- products
- trade records
- search results
- audit events.

Filtering should be explicit, for example:

~~~text
country=DE
hs_code=1801
valid_on=2026-09-01
instrument_type=regulation
status=published
~~~

Do not expose arbitrary database query syntax through the public API.

## 30. API Security

The API security baseline should include:

- TLS
- secure authentication
- authorization
- input validation
- output encoding where relevant
- rate limiting
- request size limits
- abuse protection
- secure secrets
- audit logging
- dependency security
- security headers where applicable.

## 31. API Observability

Every request should be traceable where appropriate.

Useful metadata:

- request ID
- correlation ID
- authenticated principal
- endpoint
- response status
- duration
- dependency timing
- error category.

Avoid logging passwords, access tokens, unnecessary personal data, sensitive credentials or full confidential documents unless explicitly justified.

## 32. External Service Adapters

External systems should be behind explicit adapters.

Examples:

~~~text
WTOTradeDataAdapter
ITCTradeDataAdapter
IdentityProviderAdapter
NotificationAdapter
ObjectStorageAdapter
LLMProviderAdapter
~~~

The application should not scatter provider-specific API calls throughout domain logic.

## 33. LLM Provider Boundary

The LLM should be accessed through an internal abstraction.

~~~text
AI Application Service
       ↓
LLM Provider Interface
       ↓
Provider Adapter
       ↓
Model Provider
~~~

This makes it possible to change models/providers without rewriting the application.

## 34. Event and Job Boundaries

Not every operation needs a distributed event bus.

Initially, background jobs can support:

- ingestion
- OCR
- extraction
- embedding
- indexing
- regulatory change detection
- report generation
- alert dispatch.

Events become more useful as independent consumers and scale requirements grow.

## 35. Initial Internal Architecture

~~~text
┌──────────────────────────────────────┐
│              API Layer               │
├──────────────────────────────────────┤
│         Application Services         │
├──────────────────────────────────────┤
│             Domain Layer             │
├──────────────────────────────────────┤
│      Ports / Repositories / Adapters │
├──────────────┬───────────────┬───────┤
│ Domain Store │ Search/Graph  │ Trade │
│              │ /Vector       │ Data  │
├──────────────┴───────────────┴───────┤
│       Documents / Object Storage     │
└──────────────────────────────────────┘

Background Worker Layer
  ├── ingestion
  ├── OCR
  ├── extraction
  ├── embeddings
  ├── indexing
  └── analysis
~~~

This remains one logical system.

## 36. What Should Not Become a Microservice Yet

Avoid prematurely separating classification, requirements, agreements, tariffs, evidence and scenario analysis into independently deployed services.

They share:

- transactions
- domain models
- evidence
- temporal rules
- evaluation context.

Premature distribution would add operational complexity without necessarily improving the architecture.

## 37. Future Service Extraction Signals

A module may eventually become a separate service when there is a clear reason such as:

- independent scaling
- independent deployment
- different availability requirements
- separate security boundary
- different technology/runtime requirements
- organizational ownership
- high-throughput processing.

The architecture should allow extraction without requiring it now.

## 38. API-to-Storage Rule

Application code should not routinely do:

~~~text
HTTP Controller
   ↓
SQL query
   ↓
Response
~~~

Prefer:

~~~text
HTTP Controller
   ↓
Application Service
   ↓
Domain / Repository
   ↓
Persistence
~~~

This keeps business behaviour out of transport code.

## 39. Query vs Command Separation

The architecture should distinguish operations that change state from those that retrieve/analyse state.

### Commands

Examples:

- create scenario
- publish requirement
- register source
- start ingestion
- approve knowledge
- create alert.

### Queries

Examples:

- search provisions
- retrieve requirement
- get tariff
- inspect evidence
- compare markets
- retrieve scenario result.

This separation does not require implementing full CQRS. It is primarily a design discipline.

## 40. Scenario Evaluation as a Domain Command

Evaluation can be treated as an explicit domain/application command:

~~~text
EvaluateExportScenario
      ↓
Load scenario
      ↓
Resolve context
      ↓
Evaluate rules
      ↓
Persist evaluation
      ↓
Publish result
~~~

The evaluation should record the rule/evidence context used so that results remain reproducible.

## 41. API Contract as a Boundary

The API contract should describe:

- accepted inputs
- validation rules
- response schemas
- error schemas
- authentication requirements
- authorization requirements
- pagination
- filtering
- asynchronous job behaviour.

OpenAPI can become the machine-readable contract later.

## 42. First-Release API Priorities

The first useful API surface should focus on:

1. Authentication/context
2. Products and HS codes
3. Countries/markets
4. Search
5. Regulatory instruments
6. Requirements
7. Export scenarios
8. Scenario evaluation
9. Evidence
10. AI assistant
11. Sources
12. Ingestion/review administration

Trade-data analytics can expand as datasets are onboarded.

## 43. End-to-End Example

Question:

"What requirements apply to exporting Nigerian cocoa to Germany?"

Possible flow:

~~~text
POST /assistant/messages
        ↓
Assistant Application Service
        ↓
Identify:
  Product = cocoa
  Origin = Nigeria
  Destination = Germany
        ↓
Classification Service
        ↓
Search / Knowledge Services
        ↓
Requirement Applicability Service
        ↓
Agreement / Preference Service
        ↓
Tariff / NTM Services
        ↓
Evidence Service
        ↓
Evidence Package
        ↓
LLM
        ↓
Answer + Evidence + Uncertainty
~~~

The assistant endpoint is therefore an orchestration entry point, not the location of the regulatory logic.

## 44. Architectural Invariants

The following should become development rules:

1. API controllers do not contain core domain rules.
2. Domain services do not depend on HTTP.
3. LLM output is not authoritative domain state.
4. AI retrieval must use controlled evidence assembly.
5. Authoritative data is not stored only in a derived index.
6. External providers are accessed through adapters.
7. Long-running work is asynchronous where appropriate.
8. Retried commands must be safe where idempotency is required.
9. Authorization is enforced server-side.
10. Significant evaluations produce traceable results.
11. Errors expose safe, stable API contracts.
12. Modules remain separable even when deployed together.
13. Graph/search/vector stores are derived representations unless explicitly designated otherwise.
14. Historical evaluations remain reproducible.

## 45. Next Pass

**Pass 12 — Security, Identity, Authorization & Governance Architecture**

The next pass should define:

- identity
- authentication
- authorization
- RBAC/ABAC boundaries
- organizations/tenancy
- privileged roles
- knowledge publication permissions
- audit
- data classification
- secrets
- encryption
- API security
- document security
- AI security
- prompt injection
- model/data isolation
- privacy
- incident handling
- security monitoring
- governance.

This is where the platform's government/institutional deployment requirements become much more concrete.
