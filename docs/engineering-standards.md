# Engineering Standards

## Purpose

This document establishes the engineering standards and design principles for the NG Trade Intelligence Platform.

These standards are tailored to the nature of the system: an evidence-driven, AI-assisted regulatory and trade intelligence web application that may be used in government, institutional, analytical and exporter-facing contexts.

The standards are intended to guide architecture, implementation, testing, security, data management and user experience.

They are a baseline, not a prohibition against future improvement.

---

# 1. Engineering Philosophy

The platform should be built according to the following principles:

1. **Source-first** — authoritative information remains the foundation.
2. **Secure-by-default** — security is designed into every layer.
3. **Evidence-first AI** — AI must be grounded in retrievable evidence.
4. **Human accountability** — the system assists decisions; it does not silently make authoritative legal or commercial decisions.
5. **Auditability** — important system actions and analytical outputs should be traceable.
6. **Temporal correctness** — information must be interpreted in its applicable time period.
7. **Accessibility by design** — accessibility is a core requirement, not an afterthought.
8. **Interoperability** — standards-based interfaces should be preferred.
9. **Separation of concerns** — presentation, application, domain logic, data and AI concerns should remain appropriately separated.
10. **Testability** — critical behaviour must be independently testable.
11. **Observability** — failures, data quality issues and important system behaviour must be measurable.
12. **Maintainability** — the architecture should remain understandable as the platform grows.
13. **Extensibility** — new countries, products, sources, datasets and analytical capabilities should not require fundamental redesign.
14. **Explicit uncertainty** — uncertain classifications, incomplete data and conflicting sources must not be presented as false certainty.

---

# 2. Standards Baseline

The project should use established standards and recognised best-practice frameworks where applicable.

## 2.1 Web Standards

Primary baseline:

- W3C standards
- WHATWG HTML and web-platform standards
- ECMAScript standards
- HTTP standards
- URL standards
- Semantic HTML
- Standards-compliant CSS.

The application should favour interoperable browser behaviour rather than browser-specific implementations.

## 2.2 Accessibility

Target:

**WCAG 2.2 Level AA**, subject to detailed accessibility requirements.

Accessibility applies to:

- navigation
- forms
- tables
- dashboards
- charts
- search
- notifications
- authentication
- AI interfaces
- document viewers
- administrative interfaces.

Keyboard access, focus management, semantic structure, accessible names, contrast, error identification and assistive-technology compatibility should be considered during component design.

## 2.3 Security

Primary security baseline:

**OWASP guidance and recognised application-security practices.**

The platform should incorporate:

- secure authentication
- strong authorization
- least privilege
- input validation
- output encoding
- secure session management
- CSRF protection where applicable
- protection against XSS
- protection against injection
- secure file handling
- SSRF protection
- secure secrets management
- dependency management
- security logging
- security monitoring
- secure configuration
- encryption in transit
- appropriate encryption at rest.

Security controls should be threat-modelled according to actual platform risks.

---

# 3. Architecture Standards

## 3.1 Separation of Concerns

The platform should maintain meaningful boundaries between:

- Presentation
- Application/API
- Domain/business logic
- AI orchestration
- Retrieval
- Knowledge graph
- Structured data
- Document storage
- Ingestion
- Identity/security
- Observability.

A UI component should not contain regulatory determination logic merely because it is convenient.

## 3.2 Domain Logic

Regulatory and trade rules should be represented as explicit domain logic wherever deterministic behaviour is possible.

For example:

```
Product + Origin + Destination + Date
        ↓
Applicable Rules
        ↓
Applicable Requirements
```

The LLM should not be the only mechanism determining whether a regulatory rule applies.

## 3.3 AI as a System Component

AI should be treated as an application subsystem rather than as the database or authority.

AI responsibilities may include:

- interpreting natural-language intent
- extracting entities
- selecting retrieval strategies
- synthesising evidence
- explaining results
- comparing documents
- assisting analysis.

Authoritative data, deterministic rules and provenance remain outside the model.

---

# 4. Regulatory Information Standards

This platform has requirements beyond an ordinary business web application because its information concerns laws, regulations, agreements and market-access measures.

## 4.1 Legal Instrument Identity

Every legal/regulatory instrument should have a stable identity.

The model should distinguish, where applicable:

- Act
- Regulation
- Rule
- Decree/order
- Circular
- Guideline
- Standard
- Procedure
- Treaty
- Agreement
- Protocol
- Convention
- MOU
- Notice
- Other instrument.

## 4.2 Temporal Validity

Regulatory records should support:

- publication date
- effective-from date
- effective-to date
- amendment date
- repeal date
- supersession date
- retrieval date
- version.

The system should be capable of reconstructing the applicable information for a historical date.

## 4.3 Provenance

A material regulatory claim should be traceable to:

```
Claim
 ↓
Requirement / Fact
 ↓
Provision or Data Record
 ↓
Document / Dataset
 ↓
Authoritative Source
```

The user should be able to inspect supporting evidence where appropriate.

## 4.4 Source Conflicts

The system must not silently hide conflicts.

Where sources differ, the platform should record:

- sources involved
- dates
- jurisdiction
- instrument status
- apparent conflict
- resolution rule, if one exists
- unresolved status where necessary.

---

# 5. Trade Data Standards

Trade data must preserve its analytical context.

A data record should, where available, retain:

- source
- dataset
- reporter
- partner
- product
- HS version
- HS code
- period
- trade direction
- quantity
- quantity unit
- trade value
- currency/unit conventions
- methodology
- retrieval date.

## 5.1 Classification Versioning

HS codes must be treated as versioned classifications.

The system should avoid assuming that the meaning of a code is permanently identical across HS revisions.

Mappings between versions should be explicitly represented.

## 5.2 Data Quality

The platform should distinguish:

- missing data
- zero values
- estimated values
- conflicting values
- stale values
- provisional values
- validated values.

---

# 6. API Standards

APIs should be designed around standards-based HTTP behaviour.

Where REST is used, APIs should generally provide:

- predictable resource naming
- appropriate HTTP methods/status codes
- validation
- pagination
- filtering
- sorting
- consistent error responses
- authentication/authorization
- rate limiting
- versioning strategy
- idempotency where appropriate
- machine-readable schemas.

OpenAPI should be considered for formal API contracts.

External APIs must not be treated as permanently available. Integration services should handle:

- timeouts
- retries
- rate limits
- upstream changes
- partial failure
- stale data
- source outages.

---

# 7. Frontend Standards

The web application should be:

- responsive
- accessible
- keyboard usable
- consistent
- predictable
- performant
- progressively understandable.

## 7.1 Design System

The application should eventually establish a design system covering:

- typography
- spacing
- colour
- buttons
- forms
- tables
- cards
- navigation
- alerts
- dialogs
- loading states
- error states
- empty states
- data visualisation.

Components should be reusable rather than independently reinvented.

## 7.2 Data-Heavy UX

Because the platform is fundamentally an intelligence application, special attention should be given to:

- dense tables
- filtering
- sorting
- search
- comparison
- drill-down
- citations
- source panels
- timelines
- charts
- map-based analysis where appropriate.

The interface should allow users to move from an analytical conclusion back to the underlying evidence.

---

# 8. AI Interface Standards

AI responses should be designed differently from ordinary chat applications.

A significant response may contain:

1. Answer
2. Reasoning/result explanation at an appropriate level
3. Evidence
4. Source documents
5. Data used
6. Applicable dates
7. Uncertainty/limitations
8. Suggested next actions.

The interface should avoid presenting generated text as though it were itself an authoritative regulation.

## 8.1 Citation Behaviour

Where a response depends materially on a source, the user should be able to identify the source and, where possible, the relevant provision or data record.

## 8.2 Uncertainty

The system should distinguish:

- confirmed
- inferred
- probable
- incomplete
- conflicting
- requires verification.

These labels should be based on defined system rules rather than arbitrary model wording.

---

# 9. Privacy and Data Protection

The platform should apply privacy-by-design principles.

Requirements should include:

- data minimisation
- purpose limitation
- controlled access
- appropriate retention
- secure deletion
- access auditing
- protection of user and organisation data.

If the platform processes personal data in Nigeria or other jurisdictions, applicable data-protection requirements should be identified and incorporated into the legal/compliance architecture.

---

# 10. Identity and Authorization

Authorization should be based on explicit permissions rather than UI visibility alone.

The system should eventually support:

- users
- organisations
- roles
- permissions
- scopes
- administrative roles
- service identities
- API credentials.

Critical operations should be authorized server-side.

A user hiding an administrative button must never be considered an authorization control.

---

# 11. Auditability

Important actions should produce auditable records.

Potential audit events include:

- authentication events
- authorization changes
- source changes
- document ingestion
- regulatory updates
- knowledge-model changes
- administrative actions
- configuration changes
- important analytical workflows.

For AI interactions, the system should determine which events require retention based on security, governance, privacy and operational requirements.

---

# 12. Observability

The platform should eventually provide:

### Logs

Structured machine-readable logs.

### Metrics

Examples:

- API latency
- request volume
- ingestion success/failure
- source freshness
- search latency
- retrieval quality indicators
- AI request latency
- error rates.

### Traces

Distributed tracing should be considered where the architecture contains multiple services or external integrations.

Observability should help answer:

> What happened, where did it happen, why did it happen, and what information was involved?

---

# 13. Performance

Performance should be treated as a measurable requirement.

Important areas include:

- initial page load
- search response
- dashboard rendering
- API latency
- database queries
- graph queries
- document retrieval
- AI response latency
- large-table performance.

Performance targets should be defined after actual usage patterns are understood.

---

# 14. Reliability and Resilience

External data providers are dependencies and may fail.

The system should be designed for:

- graceful degradation
- retries with limits
- timeouts
- caching
- queued ingestion
- idempotent processing
- failure isolation
- backup/recovery
- source outage visibility.

A temporary failure of an external API should not corrupt the internal knowledge base.

---

# 15. Data Ingestion Standards

Ingestion pipelines should be:

- repeatable
- observable
- idempotent
- version-aware
- provenance-preserving
- failure-tolerant.

A source update should not simply overwrite the previous state without preserving the necessary history.

Conceptually:

```
Source
 ↓
Acquire
 ↓
Validate
 ↓
Normalise
 ↓
Classify
 ↓
Extract
 ↓
Relate
 ↓
Index
 ↓
Publish
 ↓
Monitor
```

---

# 16. Document Intelligence Standards

Documents may arrive as:

- PDF
- HTML
- Word documents
- spreadsheets
- scanned documents
- structured API responses
- other official formats.

The system should preserve the original source artifact where permitted.

For extracted information, retain appropriate relationships between:

- source document
- page/section
- extracted text
- provision
- structured fact
- knowledge-graph entity.

OCR-derived information should be distinguishable from digitally authored text where that distinction affects confidence.

---

# 17. Testing Standards

Testing should occur at multiple levels:

### Unit testing

Deterministic business rules and domain logic.

### Integration testing

Databases, APIs, search, graph, storage and external integrations.

### End-to-end testing

Important user workflows.

### Security testing

Authentication, authorization, input handling, dependency and application security.

### Accessibility testing

Automated checks plus manual/assistive-technology testing.

### AI evaluation

AI-specific evaluation should include:

- grounding
- citation correctness
- retrieval quality
- factual consistency
- refusal/uncertainty behaviour
- regression testing
- adversarial prompts.

A technically correct application with unreliable regulatory answers is not acceptable.

---

# 18. AI/LLM Governance

AI components should have explicit controls for:

- model identification
- prompt/version management
- retrieval configuration
- evaluation
- output validation
- sensitive-data handling
- logging policy
- model/provider changes
- fallback behaviour.

Changing an AI model should be treated as an engineering change that may require regression evaluation.

---

# 19. Supply-Chain and Dependency Security

The project should maintain control over software dependencies.

Practices should include:

- dependency pinning/controlled versions
- vulnerability scanning
- update management
- software composition analysis where appropriate
- secret scanning
- code review
- protected branches
- reproducible builds where practical.

Third-party packages should not be introduced merely for convenience without considering maintenance and security implications.

---

# 20. Git and Development Practices

The repository should eventually use:

- meaningful commits
- pull requests where appropriate
- code review
- protected main branch
- issue tracking
- documented architectural decisions
- automated CI
- automated tests
- linting/formatting
- security checks.

Architecture decisions that materially affect the system should be recorded as ADRs.

---

# 21. Internationalisation and Localisation

Although the first deployment is Nigeria-focused, the system should avoid unnecessarily embedding English-only assumptions into the domain model.

The architecture should be capable of supporting:

- multiple languages
- jurisdiction-specific terminology
- local date/number/currency formats
- multilingual source documents
- translated UI/content where required.

Internationalisation should be considered early even if multilingual support is not part of the first release.

---

# 22. Explainability and Human Oversight

The platform should help users understand:

- what the system found
- why it considers information relevant
- which rules were applied
- which sources support the result
- what is uncertain
- what requires human verification.

For regulatory and compliance scenarios, the system should avoid presenting an AI-generated conclusion as a substitute for authoritative legal interpretation.

---

# 23. Governance of the Knowledge Base

Knowledge should have controlled lifecycle states.

A possible lifecycle:

```
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

Not every source will require the same level of human review. Review requirements should depend on source authority, data type and intended use.

---

# 24. Design Principle: Follow the Evidence

A core interaction pattern for the platform should be:

```
Insight
  ↓
Explanation
  ↓
Supporting Fact
  ↓
Provision / Data Record
  ↓
Source
```

This should become a defining UX characteristic of the platform.

The system should make it easy to move from **"What does the platform say?"** to **"Why does it say that?"**

---

# 25. Standards Decision Hierarchy

When choosing between implementation approaches, use this order:

1. Applicable law/regulation
2. Required institutional policy
3. Relevant international/industry standard
4. Security/accessibility requirements
5. Domain requirements
6. Architectural consistency
7. Maintainability
8. Performance
9. Developer convenience.

Convenience should not override a higher-order requirement.

---

# 26. Standards Governance

These standards are living project documentation.

They should be reviewed whenever the project:

- introduces a major subsystem
- changes its security model
- introduces AI capabilities
- adds a new jurisdiction
- adds new categories of personal data
- changes deployment architecture
- introduces major external integrations.

Material deviations should be documented rather than silently introduced.

---

## Initial Standards Baseline

| Area | Baseline |
|---|---|
| Web | W3C / WHATWG / relevant web standards |
| Accessibility | WCAG 2.2 AA target |
| Security | OWASP guidance + threat modelling |
| HTTP/API | HTTP semantics + OpenAPI where appropriate |
| Data | Provenance, integrity, versioning, temporal validity |
| AI | Evidence-grounded, evaluated, auditable |
| UX | Accessible, responsive, evidence-traceable |
| Testing | Unit + integration + E2E + security + accessibility + AI evaluation |
| Observability | Logs + metrics + traces where appropriate |
| Development | Git, review, CI, testing, ADRs |
| Privacy | Privacy-by-design and applicable data-protection requirements |
| Reliability | Resilience, graceful degradation and recoverability |

## Status

**Document:** Engineering Standards

**Stage:** Foundation

**Status:** Living document

These standards establish the engineering baseline before detailed implementation decisions are made.
