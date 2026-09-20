# Pass 9 — Domain Rules & Applicability Engine

## 1. Purpose

This pass defines the deterministic business/domain logic that determines whether trade rules, requirements, agreements, preferences, tariffs and non-tariff measures apply to an export scenario.

The engine is deliberately separated from the AI layer.

AI may interpret questions, assist retrieval and explain results. The applicability engine is responsible for deterministic decisions wherever the underlying rules and evidence are sufficiently structured.

## 2. Core Evaluation Model

An export scenario is evaluated using:

```text
Product
+ HS Code
+ Origin
+ Destination
+ Scenario Date
+ Exporter Context
+ Quantity / Value where relevant
+ Processing / Origin facts where relevant
+ Intended Use where relevant
        ↓
Applicable legal/regulatory context
        ↓
Requirements
+ Agreements
+ Preferences
+ Tariffs
+ NTMs
+ Conditions
        ↓
Evidence-backed result
```

The engine must never assume that a rule applies merely because the entities are related.

## 3. Applicability Is Contextual

A requirement is not simply:

`Requirement → Product`

It is better represented as:

```text
Requirement
   ↓
Applicability Rule
   ↓
Product + Origin + Destination + Date + Conditions
   ↓
Applicable / Not Applicable / Unresolved
```

The same requirement can apply to one export scenario and not another.

## 4. Required Evaluation Context

### Mandatory
- product
- origin country
- destination market
- scenario date

### Strongly preferred
- HS code
- exporter type
- quantity
- value
- processing state
- intended use

### Optional
- agreement claimed
- preference claimed
- certificate availability
- previous compliance status
- special market/customer conditions

If a rule requires information that is missing, the engine should return **Unresolved** rather than guessing.

## 5. Evaluation Result States

Every deterministic applicability evaluation should produce one of:

- **Applicable** — sufficient evidence and rule conditions establish that the rule applies.
- **Not Applicable** — sufficient evidence establishes that the rule does not apply.
- **Unresolved** — the rule may apply, but required facts or evidence are insufficient.
- **Insufficient Evidence** — a potentially relevant rule was identified but cannot be established from available authoritative evidence.
- **Conflicting** — relevant authoritative sources produce materially conflicting states that cannot safely be resolved automatically.

These states must not be collapsed into a simple Boolean.

## 6. Rule Structure

An applicability rule conceptually contains:

```text
RULE
 ├── target
 ├── conditions
 ├── effective period
 ├── priority / precedence
 ├── result semantics
 ├── exceptions
 ├── evidence
 └── rule version
```

Candidate fields:
- rule_id
- rule_type
- target_type
- target_id
- condition_set
- valid_from
- valid_to
- priority
- rule_version
- status
- evidence references

## 7. Condition Evaluation

Conditions should be evaluated individually before producing an overall result.

Example:

```text
Requirement R1
  Product = Cocoa
  AND Origin = Nigeria
  AND Destination = Market X
  AND Date >= 2026-01-01
  AND HS Code ∈ {1801.xx}
        ↓
Each condition evaluated
        ↓
All mandatory conditions satisfied
        ↓
Applicable
```

Possible operators:
- equals
- not_equals
- in
- not_in
- greater_than
- greater_than_or_equal
- less_than
- less_than_or_equal
- between
- exists
- does_not_exist
- matches
- overlaps

## 8. Three-Valued Logic

Ordinary true/false logic is insufficient because trade information can be unknown.

The engine should support:

```text
TRUE
FALSE
UNKNOWN
```

Example:

`Origin = Nigeria` → TRUE

`Destination = Germany` → TRUE

`Processing satisfies rule of origin` → UNKNOWN

Overall eligibility cannot safely become TRUE when a mandatory condition is UNKNOWN.

Therefore:

```text
TRUE + TRUE + UNKNOWN
            ↓
         UNKNOWN
```

This is particularly important for rules of origin and product-specific conditions.

## 9. Rule Composition

Support explicit logical groups:

```text
AND
OR
NOT
EXISTS
FOR_ALL
```

Example:

```text
Certificate required IF
    Product = P
    AND Destination = M
    AND
       (Exporter Type = A OR Exporter Type = B)
```

Nested condition groups should be possible without requiring code changes for every new rule.

## 10. Rule Precedence

When multiple rules affect the same scenario, the engine needs explicit precedence.

Suggested computational precedence:

1. More specific rule over general rule
2. Effective/current rule over expired rule
3. Later valid amendment over earlier superseded provision
4. Explicit exception over general condition
5. Higher-authority applicable source where legally relevant
6. Human-verified rule over unverified extraction
7. Otherwise surface the conflict

**Precedence must be treated as a domain rule, not an arbitrary database ordering.**

## 11. Temporal Evaluation

The engine must evaluate rules against the scenario date.

Conceptually:

```text
rule.valid_from <= scenario_date
AND
(rule.valid_to IS NULL OR scenario_date < rule.valid_to)
```

Legal effective dates and source publication dates must remain distinct.

Example:

```text
Published: 2025-10-01
Effective: 2026-01-01
Scenario: 2025-12-15
        ↓
Rule exists in source corpus
but is not yet effective for the scenario.
```

Historical scenarios must remain reproducible.

## 12. Instrument Lifecycle Rules

Regulatory instruments can:
- amend another instrument
- supersede another instrument
- repeal another instrument
- implement an agreement
- reference another instrument

The engine must not simply select the newest document. It must determine which instrument was legally/effectively applicable at the scenario date.

## 13. Requirement Evaluation

Basic algorithm:

```text
1. Identify candidate requirements
2. Filter by temporal validity
3. Filter by jurisdiction/market
4. Filter by product/HS scope
5. Evaluate origin conditions
6. Evaluate destination conditions
7. Evaluate exporter/context conditions
8. Evaluate exceptions
9. Evaluate evidence sufficiency
10. Produce result
11. Attach evidence
```

Candidate retrieval should be broad enough that relevant rules are not prematurely discarded. Final applicability should be deterministic wherever possible.

## 14. HS Classification Logic

Classification is a prerequisite for many downstream rules.

States:

```text
Candidate
   ↓
Suggested
   ↓
Confirmed

Possible alternate states:
Disputed
Unresolved
```

AI can suggest classifications from product descriptions, but must not automatically promote a suggestion to confirmed status.

Downstream tariff/preference/requirement evaluation should expose classification uncertainty.

Example:

```text
HS Classification = Suggested
        ↓
Tariff result
        ↓
Classification-dependent / requires confirmation
```

## 15. Agreement Applicability

Agreement applicability must be evaluated in stages:

```text
1. Is the agreement in force?
2. Is the origin a party?
3. Is the destination covered?
4. Is the product/HS code covered?
5. Are relevant preference provisions active?
6. Are origin rules satisfied?
7. Are other eligibility conditions satisfied?
8. Is the preference actually available for this scenario?
```

Agreement participation alone is insufficient.

## 16. Preference Eligibility

Preference evaluation should produce separate states:

```text
Agreement applicable
        ↓
Product covered
        ↓
Origin requirement satisfied
        ↓
Preference condition satisfied
        ↓
Preference available
```

If origin evidence is missing:

`Preference = Unresolved`

not:

`Preference = Not Available`.

## 17. Rules of Origin

Rules of origin can contain complex conditions, including:
- wholly obtained
- substantial transformation
- change in tariff classification
- regional value content
- specific processing
- combinations of conditions

The engine should represent these as structured rule components rather than forcing the LLM to determine eligibility from prose each time.

Where required inputs are unavailable, the result remains unresolved.

## 18. Tariff Selection

Tariff selection should consider:
- destination
- origin
- HS code
- tariff regime
- preference eligibility
- effective date
- quota where relevant

Conceptually:

```text
Candidate tariff records
        ↓
Destination match
        ↓
Origin/regime match
        ↓
HS match
        ↓
Date match
        ↓
Preference eligibility
        ↓
Applicable tariff
```

Do not simply select the lowest rate. The engine must establish why a particular tariff treatment is applicable.

## 19. NTM Applicability

Non-tariff measures should be evaluated independently of tariffs.

Examples:
- sanitary/phytosanitary
- technical requirements
- labelling
- packaging
- certification
- inspection
- licensing
- registration

NTM applicability may depend on product, destination, intended use, exporter characteristics and other conditions.

## 20. Requirement Aggregation

A scenario may produce multiple requirements from different sources.

Aggregate them without losing source identity:

```text
Nigerian export requirement
        +
Destination requirement
        +
Agreement requirement
        +
Product-specific requirement
        ↓
Combined requirement set
```

Duplicate requirements should be detected carefully. Similar descriptions do not prove identical legal bases.

## 21. Conflicting Rules and Sources

When relevant sources conflict:

1. Identify the conflict.
2. Preserve both source assertions.
3. Evaluate temporal validity.
4. Evaluate amendment/supersession relationships.
5. Apply documented precedence rules where available.
6. If unresolved, return **Conflicting** or **Unresolved**.
7. Present the conflicting evidence to the user.

The AI must not silently choose one source merely because it produces a more plausible answer.

## 22. Evidence Sufficiency

Every important deterministic result should be classified by evidence state:

- confirmed
- supported
- incomplete
- conflicting
- inferred
- requires_verification

Example:

```text
Requirement R1
Result: Applicable
Evidence: Official provision
Verification: Human reviewed
Validity: 2026-01-01 → present
```

Another:

```text
Preference P1
Result: Unresolved
Reason: Required origin criterion not established
Evidence: Agreement provision available
Missing fact: processing history
```

## 23. Deterministic vs AI Responsibilities

### Deterministic engine

Responsible for:
- temporal filtering
- status filtering
- HS-version matching
- structured condition evaluation
- tariff selection
- aggregation
- agreement state
- preference eligibility where rules are structured
- permissions
- audit
- workflow state

### AI layer

Assists with:
- natural-language question understanding
- entity extraction
- ambiguous product interpretation
- retrieval planning
- summarisation
- explanation
- comparison
- synthesis
- identifying potentially missing information

### Shared boundary

AI may propose structured facts or rules for review. It should not silently publish them as authoritative domain rules.

## 24. AI-Assisted Rule Extraction

Regulatory documents will often contain rules that are difficult to manually encode.

Proposed pipeline:

```text
Source Document
      ↓
OCR / Text Extraction
      ↓
Provision Segmentation
      ↓
AI Rule Candidate Extraction
      ↓
Structured Rule Representation
      ↓
Validation
      ↓
Human Review where required
      ↓
Published Rule
      ↓
Applicability Engine
```

AI extraction creates a **candidate**, not an authoritative rule.

## 25. Rule Versioning

Rules should be versioned independently of application software releases.

Candidate fields:
- rule_id
- rule_version
- effective_from
- effective_to
- created_at
- retired_at
- status
- source_evidence

This allows historical evaluations to be reproduced using the rule set valid for the relevant period.

## 26. Evaluation Trace

Every significant evaluation should be explainable as a trace.

Example:

```text
Scenario S123
  ↓
HS Code 1801.xx
  ↓
Requirement R456
  ↓
Rule R456-V3
  ↓
Origin = Nigeria → TRUE
Destination = Market X → TRUE
Scenario Date within validity → TRUE
HS Code within scope → TRUE
Exception → FALSE
  ↓
Result = APPLICABLE
  ↓
Evidence = Provision 4.2 of Document D789
```

This trace becomes the foundation for explainability, audit and AI grounding.

## 27. Scenario Evaluation Pipeline

```text
Export Scenario
      ↓
Normalize Inputs
      ↓
Resolve Product / HS Context
      ↓
Build Temporal Context
      ↓
Retrieve Candidate Rules
      ↓
Evaluate Conditions
      ↓
Resolve Precedence
      ↓
Evaluate Agreements / Preferences
      ↓
Evaluate Tariffs / NTMs
      ↓
Assess Evidence
      ↓
Aggregate Results
      ↓
Produce Evaluation Trace
      ↓
AI Explanation / Analysis
```

## 28. Missing Information Handling

The engine should explicitly identify missing information.

Example:

```text
Requirement identified
Origin criteria available
Destination available
HS code available
Processing history missing
        ↓
Cannot determine origin eligibility
        ↓
Result = UNRESOLVED
        ↓
Required information = processing history
```

This is preferable to making assumptions.

## 29. Rule Precedence vs Legal Authority

Technical rule precedence must not be confused with legal authority.

The engine may rank candidate rules computationally for evaluation, but must preserve actual legal/source relationships.

Examples:
- a later document does not automatically supersede earlier law
- agency guidance does not automatically override legislation
- a secondary source does not become primary merely because it is easier to retrieve

Where legal hierarchy cannot be deterministically established, surface the relationship and uncertainty rather than inventing a hierarchy.

## 30. Output Contract

A domain evaluation should conceptually return:

```text
EvaluationResult
 ├── scenario_id
 ├── evaluation_timestamp
 ├── rule_set_version
 ├── result
 ├── findings[]
 │     ├── subject
 │     ├── result
 │     ├── conditions[]
 │     ├── evidence[]
 │     └── uncertainty
 ├── missing_information[]
 ├── conflicts[]
 └── evaluation_trace
```

The API implementation can later map this contract into JSON, database records and UI representations.

## 31. Core Domain Invariants

The following should become enforceable invariants:

1. No applicable requirement without a traceable rule/evidence path.
2. No preference eligibility without an applicable agreement basis.
3. No tariff conclusion without product classification context.
4. No historical evaluation using rules that were not effective at the scenario date.
5. Unknown mandatory conditions cannot be silently treated as true.
6. AI-generated facts cannot automatically become authoritative.
7. Superseded/repealed instruments remain historically retrievable.
8. Conflicting authoritative evidence is preserved.
9. Missing data is never silently interpreted as zero.
10. Every published deterministic result is reproducible from its inputs, rules and evidence.

## 32. First Business-Logic Modules

The domain layer can eventually be decomposed into:

```text
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
```

These are logical boundaries, not necessarily separate microservices. Initially they should likely exist within one application/domain service boundary.

## 33. First-Release Evaluation Sequence

```text
1. Validate scenario
2. Resolve/confirm HS code
3. Establish origin/destination
4. Establish scenario date
5. Retrieve applicable Nigerian requirements
6. Retrieve destination requirements
7. Identify relevant agreements
8. Evaluate preference eligibility
9. Retrieve applicable tariffs
10. Retrieve relevant NTMs
11. Assemble evidence
12. Produce deterministic evaluation
13. Ask AI layer to explain/summarise
```

## 34. What the AI Should See

The LLM should receive a structured evidence package rather than an unrestricted database dump.

```text
EVIDENCE PACKAGE
 ├── Scenario
 ├── Applicable rules
 ├── Evaluated conditions
 ├── Requirements
 ├── Agreement findings
 ├── Preference findings
 ├── Tariff findings
 ├── NTM findings
 ├── Source provisions
 ├── Data records
 ├── Conflicts
 └── Missing information
```

The AI then produces a human-readable explanation grounded in that package.

## 35. Next Pass

**Pass 10 — Source Acquisition, Ingestion & Knowledge Lifecycle**

The next pass should define how the platform actually acquires and turns authoritative information into governed knowledge.

Focus areas:
- source registry
- source discovery
- acquisition
- document storage
- API ingestion
- OCR
- parsing
- document segmentation
- provision extraction
- entity extraction
- rule extraction
- validation
- human review
- publication
- amendment detection
- supersession detection
- reprocessing
- data quality
- provenance

This connects the architecture to the real-world problem of continuously bringing Nigerian and international trade information into the platform.