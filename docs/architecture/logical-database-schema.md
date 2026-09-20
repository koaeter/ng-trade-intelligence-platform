# Pass 8 — Logical Database Schema

## 1. Purpose

This pass converts the domain and persistence models into a concrete logical relational schema without committing to ORM syntax, migrations, SQL dialect details, or a final physical deployment design.

The schema is designed around four principles:
- authoritative ownership
- explicit relationships
- temporal correctness
- provenance and evidence traceability.

## 2. Schema Domains

The database is divided conceptually into:

1. Identity and access
2. Reference and classification
3. Regulatory knowledge
4. Agreements and market access
5. Evidence and provenance
6. Source and document ingestion
7. Trade datasets
8. Export scenarios and analysis
9. Audit and operational state.

These are logical domains. They may later become database schemas/modules rather than separate physical databases.

---

# 3. Identity and Access

## user

Represents an authenticated platform user.

Candidate fields:
- id
- external_identity_id
- email
- display_name
- status
- created_at
- updated_at
- last_login_at.

Do not store authentication secrets here if an external identity provider is used.

## role

Fields:
- id
- code
- name
- description
- status.

Examples:
- exporter
- researcher
- trade_analyst
- government_trade_officer
- compliance_officer
- policy_analyst
- source_administrator
- data_steward
- system_administrator
- security_administrator.

## permission

Fields:
- id
- code
- name
- resource
- action
- description.

## user_role

Associates users with roles.

Fields:
- user_id
- role_id
- assigned_at
- assigned_by
- valid_from
- valid_to.

## role_permission

Associates roles with permissions.

Fields:
- role_id
- permission_id.

Authorization should be evaluated separately from business applicability.

---

# 4. Geographic and Reference Data

## country

Fields:
- id
- iso_alpha2
- iso_alpha3
- iso_numeric
- name
- official_name
- status.

External identifiers should be stored separately where different systems use different country codes.

## market

A market is not necessarily identical to a country.

Fields:
- id
- name
- market_type
- country_id
- description
- status.

Examples of market types:
- country
- customs_union
- regional_market
- economic_bloc
- regulatory_jurisdiction.

## agency

Fields:
- id
- name
- acronym
- jurisdiction
- country_id
- agency_type
- official_url
- status.

An agency can administer requirements without necessarily being the source that legally establishes them.

---

# 5. Product and HS Classification

## product

Represents a platform-level product concept.

Fields:
- id
- name
- description
- product_type
- status
- created_at
- updated_at.

A product should not be assumed to have one permanent HS code.

## hs_nomenclature

Represents a classification system/version family.

Fields:
- id
- name
- publisher
- version
- effective_from
- effective_to
- source_id
- status.

Examples can include different HS editions.

## hs_code

Fields:
- id
- hs_nomenclature_id
- code
- description
- level
- parent_hs_code_id
- valid_from
- valid_to
- status.

Logical uniqueness:

`(hs_nomenclature_id, code)`

## product_hs_classification

Links a product concept to one or more HS codes.

Fields:
- id
- product_id
- hs_code_id
- classification_status
- basis
- evidence_id
- valid_from
- valid_to
- reviewed_by
- reviewed_at.

Classification status:
- candidate
- suggested
- confirmed
- disputed
- unresolved.

An AI suggestion must never silently become a confirmed classification.

## hs_code_mapping

Represents an explicit mapping between classification versions.

Fields:
- id
- source_hs_code_id
- target_hs_code_id
- mapping_type
- mapping_basis
- evidence_id
- status.

Possible mapping types:
- exact
- split
- merge
- partial
- approximate
- not_mappable.

---

# 6. Regulatory Knowledge

## regulatory_instrument

Represents a legal/regulatory instrument or formally governed instrument.

Fields:
- id
- instrument_type
- title
- short_title
- issuing_agency_id
- jurisdiction_market_id
- identifier
- publication_date
- effective_from
- effective_to
- status
- source_document_id
- created_at
- updated_at.

Instrument type must remain explicit.

Examples:
- Act
- Regulation
- Rule
- Order
- Decree
- Circular
- Guideline
- Standard
- Procedure
- Treaty
- Agreement
- Protocol
- Convention
- MOU
- Notice.

## provision

Represents a legally or institutionally meaningful provision extracted from an instrument.

Fields:
- id
- regulatory_instrument_id
- parent_provision_id
- provision_type
- provision_number
- heading
- text
- sequence
- source_location
- effective_from
- effective_to
- status.

`parent_provision_id` permits hierarchical structures without assuming that every instrument uses the same legal hierarchy.

## regulatory_topic

Fields:
- id
- name
- description.

## provision_topic

Associates provisions with topics.

Fields:
- provision_id
- topic_id.

## requirement

Represents a governed requirement derived from one or more provisions or authoritative sources.

Fields:
- id
- name
- description
- requirement_type
- administering_agency_id
- status
- valid_from
- valid_to.

Important distinction:

`Provision` = what the source says.

`Requirement` = normalized domain representation of what an exporter may need to satisfy.

## requirement_source

Associates a requirement with the provisions/evidence establishing it.

Fields:
- requirement_id
- provision_id
- evidence_record_id.

## requirement_condition

Represents structured conditions used in deterministic applicability evaluation.

Fields:
- id
- requirement_id
- condition_type
- operator
- value_type
- value_reference
- value_text
- valid_from
- valid_to.

Condition types may include:
- product
- HS code
- origin
- destination
- date
- quantity
- processing
- exporter_type
- intended_use
- agreement
- preference.

---

# 7. Regulatory Lifecycle

## instrument_relationship

Represents relationships between instruments.

Fields:
- id
- source_instrument_id
- target_instrument_id
- relationship_type
- effective_from
- effective_to
- evidence_record_id.

Relationship types include:
- amends
- supersedes
- repeals
- implements
- references
- complements.

This is preferable to embedding legal history in a simple status field.

---

# 8. Agreements and Preferences

## agreement

Represents an agreement, treaty, protocol or similar instrument at the domain level.

Fields:
- id
- regulatory_instrument_id
- name
- agreement_type
- status
- signed_date
- entry_into_force_date
- termination_date.

The associated regulatory instrument retains the authoritative textual/legal representation.

## agreement_party

Fields:
- agreement_id
- country_id
- party_role
- joined_at
- exited_at.

Party roles can distinguish original parties, acceding parties and other statuses.

## agreement_coverage

Represents products/HS codes covered by an agreement.

Fields:
- id
- agreement_id
- hs_code_id
- coverage_type
- conditions
- valid_from
- valid_to
- evidence_record_id.

## preference

Represents a preferential market-access treatment.

Fields:
- id
- agreement_id
- name
- preference_type
- origin_country_id
- destination_market_id
- hs_code_id
- rate
- rate_unit
- valid_from
- valid_to
- status.

## preference_condition

Structured eligibility conditions for a preference.

Fields:
- id
- preference_id
- condition_type
- operator
- value_type
- value_reference
- value_text.

Do not infer preference eligibility from agreement participation alone.

---

# 9. Tariffs and Non-Tariff Measures

## tariff

Fields:
- id
- hs_code_id
- origin_country_id
- destination_market_id
- tariff_type
- rate
- rate_unit
- quota_reference
- valid_from
- valid_to
- dataset_id
- source_record_id
- status.

Tariff types might include:
- MFN
- preferential
- bound
- applied
- quota rate
- other documented tariff treatment.

## ntm

Represents a non-tariff measure or market-access measure.

Fields:
- id
- ntm_type
- name
- description
- destination_market_id
- administering_agency_id
- valid_from
- valid_to
- status.

## ntm_product_scope

Fields:
- ntm_id
- hs_code_id
- scope_type
- valid_from
- valid_to.

---

# 10. Sources and Documents

## source

Represents the originating authority or information source.

Fields:
- id
- name
- source_type
- authority_level
- organization
- base_url
- jurisdiction
- reliability_status
- status.

Authority level is metadata, not a universal legal ranking.

## source_identifier

Stores identifiers used by external systems.

Fields:
- id
- source_id
- identifier_type
- identifier_value
- resource_type.

## document

Represents an acquired source artifact.

Fields:
- id
- source_id
- title
- document_type
- publication_date
- acquisition_date
- checksum
- mime_type
- storage_reference
- processing_status
- ocr_status
- version_label
- supersedes_document_id.

The document record is metadata; the actual PDF/image/etc. belongs in object storage.

## document_location

Identifies a specific location within a source artifact.

Fields:
- id
- document_id
- page_number
- section
- paragraph
- table_reference
- character_start
- character_end.

This supports evidence pointing to precise source locations.

---

# 11. Evidence and Provenance

## evidence_record

Represents a traceable piece of evidence supporting an assertion.

Fields:
- id
- evidence_type
- source_id
- document_id
- dataset_id
- data_record_id
- document_location_id
- extracted_text
- evidence_state
- verification_status
- captured_at.

Evidence type examples:
- provision
- dataset_record
- official_statement
- structured_fact
- extracted_text.

## assertion

Represents a proposition about the domain.

Fields:
- id
- subject_type
- subject_id
- predicate
- object_type
- object_id
- assertion_type
- evidence_state
- verification_status
- valid_from
- valid_to
- created_at.

## assertion_evidence

Associates assertions with evidence.

Fields:
- assertion_id
- evidence_record_id
- support_type.

Support types:
- supports
- contradicts
- qualifies.

This permits conflicting evidence to be represented rather than silently discarded.

---

# 12. Dataset and Ingestion Model

## dataset

Fields:
- id
- source_id
- name
- description
- dataset_type
- update_frequency
- documentation_url
- status.

## dataset_version

Fields:
- id
- dataset_id
- version_label
- published_at
- retrieved_at
- effective_from
- effective_to
- checksum
- status.

## ingestion_job

Defines an ingestion process.

Fields:
- id
- dataset_id
- job_type
- configuration
- schedule
- status.

## ingestion_run

Represents one execution.

Fields:
- id
- ingestion_job_id
- dataset_version_id
- started_at
- completed_at
- status
- records_received
- records_accepted
- records_rejected
- error_summary.

## source_record

Represents the raw/source-level record.

Fields:
- id
- dataset_version_id
- external_record_id
- raw_reference
- raw_payload_reference
- checksum
- retrieved_at.

## data_quality_issue

Fields:
- id
- ingestion_run_id
- source_record_id
- issue_type
- severity
- description
- status
- resolved_at.

---

# 13. Canonical Trade Data

## trade_record

Represents a normalized trade observation.

Fields:
- id
- dataset_version_id
- reporter_country_id
- partner_country_id
- hs_code_id
- period
- trade_direction
- quantity
- quantity_unit
- trade_value
- currency
- value_convention
- data_status
- source_record_id.

Data status must distinguish:
- observed
- estimated
- provisional
- revised
- missing
- suppressed
- conflicting.

Critical rule:

`missing ≠ zero`

`suppressed ≠ zero`

`estimated ≠ observed`.

---

# 14. Export Scenarios

## export_scenario

Represents a user-defined export question/context.

Fields:
- id
- created_by_user_id
- organization_id
- product_id
- origin_country_id
- destination_market_id
- hs_code_id
- scenario_date
- quantity
- quantity_unit
- intended_use
- exporter_type
- status
- created_at
- updated_at.

## scenario_input

Stores explicit inputs that do not fit fixed columns or need versioned representation.

Fields:
- id
- scenario_id
- input_type
- value_type
- value_reference
- value_text
- source.

## applicability_evaluation

Represents a deterministic evaluation of a requirement against a scenario.

Fields:
- id
- scenario_id
- requirement_id
- result
- evaluation_version
- evaluated_at
- rule_reference
- evidence_state.

Results:
- applicable
- not_applicable
- unresolved
- insufficient_evidence.

## scenario_evidence

Associates scenario results with evidence.

Fields:
- scenario_id
- evidence_record_id
- relevance_type.

## scenario_result

Represents a persisted analytical result.

Fields:
- id
- scenario_id
- result_type
- result_version
- generated_at
- status
- summary_reference.

The result is derived. It is not an authoritative source.

---

# 15. Saved Research and Alerts

## saved_research

Fields:
- id
- user_id
- title
- description
- query_reference
- saved_at.

## alert_subscription

Fields:
- id
- user_id
- product_id
- destination_market_id
- alert_type
- criteria
- status
- created_at.

Examples:
- regulatory change
- tariff change
- agreement change
- market indicator change.

---

# 16. Audit

## audit_event

Fields:
- id
- actor_user_id
- actor_type
- action
- resource_type
- resource_id
- occurred_at
- request_id
- outcome
- metadata_reference.

Audit events should be append-oriented and protected from ordinary application modification.

---

# 17. Core Relationships

```text
PRODUCT
  └── product_hs_classification ──> HS_CODE
                                      │
                                      └── HS_NOMENCLATURE

REGULATORY_INSTRUMENT
  ├── contains ──> PROVISION
  ├── amends ──> REGULATORY_INSTRUMENT
  ├── supersedes ──> REGULATORY_INSTRUMENT
  └── issued_by ──> AGENCY

PROVISION
  └── establishes/supports ──> REQUIREMENT
                                  │
                                  ├── administered_by ──> AGENCY
                                  └── conditions ──> REQUIREMENT_CONDITION

AGREEMENT
  ├── agreement_party ──> COUNTRY
  ├── agreement_coverage ──> HS_CODE
  └── provides ──> PREFERENCE

PREFERENCE
  └── preference_condition

TARIFF
  ├── HS_CODE
  ├── origin COUNTRY
  └── destination MARKET

EVIDENCE_RECORD
  ├── SOURCE
  ├── DOCUMENT
  ├── DATASET
  └── DATA_RECORD

ASSERTION
  └── assertion_evidence ──> EVIDENCE_RECORD

EXPORT_SCENARIO
  ├── PRODUCT
  ├── origin COUNTRY
  ├── destination MARKET
  ├── HS_CODE
  └── applicability_evaluation ──> REQUIREMENT
```

---

# 18. Referential Integrity Rules

Important constraints:

1. A provision must belong to a regulatory instrument.
2. A requirement must have a traceable source/evidence path before publication.
3. An HS code must belong to a defined nomenclature/version.
4. A product classification should not reference an inactive/nonexistent HS code.
5. A preference must reference a defined agreement.
6. A tariff must reference a defined product classification and market context.
7. A trade record must reference its dataset version.
8. Evidence must identify its source path.
9. Scenario evaluations must reference the scenario and requirement used.
10. Published knowledge must not depend solely on transient AI output.

---

# 19. Temporal Rules

Temporal fields must not be collapsed into one generic date.

Use distinct concepts:
- published_at
- retrieved_at
- effective_from
- effective_to
- valid_from
- valid_to
- amended_at
- superseded_at
- observation_period.

An object can be retrieved today while describing a rule that became effective years earlier.

Scenario evaluation should therefore accept an explicit scenario date.

---

# 20. Graph Projection Mapping

The relational model remains authoritative for governed structured entities.

Potential graph projection:

| Relational entity | Graph node |
|---|---|
| product | Product |
| hs_code | HS Code |
| country | Country |
| market | Market |
| agency | Agency |
| regulatory_instrument | Regulatory Instrument |
| provision | Provision |
| requirement | Requirement |
| agreement | Agreement |
| preference | Preference |
| source | Source |
| document | Document |
| evidence_record | Evidence Record |
| assertion | Assertion |

Relationship tables become typed graph edges.

Graph projection must preserve the authoritative relational identifier so every graph object can be traced back to its source record.

---

# 21. Search Projection Mapping

Potential searchable documents:
- regulatory instrument
- provision
- requirement
- agreement
- product
- source document
- selected trade indicators.

Search documents should contain enough metadata for filtering:
- jurisdiction
- instrument type
- source
- publication date
- effective date
- product
- HS code
- country/market
- evidence state.

Embeddings are derived artifacts and must be reproducible from source content.

---

# 22. What Should NOT Be Stored as Authoritative Data

The following should not automatically become authoritative merely because the system generated them:

- LLM answers
- AI classifications
- generated summaries
- generated market narratives
- inferred relationships
- cached search results
- cached tariff calculations.

These may be stored as derived results with provenance and version information.

---

# 23. Initial Schema Boundary

The first implementation does not need every proposed table.

Minimum relational foundation:

```text
user
role
permission
user_role
role_permission

country
market
agency

product
hs_nomenclature
hs_code
product_hs_classification
hs_code_mapping

source
document
document_location
regulatory_instrument
provision
requirement
requirement_condition
instrument_relationship

agreement
agreement_party
agreement_coverage
preference
preference_condition

tariff
ntm
ntm_product_scope

evidence_record
assertion
assertion_evidence

dataset
dataset_version
ingestion_job
ingestion_run
source_record
data_quality_issue
trade_record

export_scenario
scenario_input
applicability_evaluation
scenario_evidence
scenario_result

saved_research
alert_subscription
audit_event
```

---

# 24. Important Design Decision

The schema deliberately separates:

**Source truth**
→ documents, provisions, authoritative datasets

**Normalized domain knowledge**
→ requirements, products, classifications, agreements, preferences

**Evaluation**
→ scenario-specific applicability results

**Derived intelligence**
→ findings, summaries, AI responses, analytical results.

This prevents a common failure mode in AI systems where generated conclusions gradually become indistinguishable from source facts.

---

# 25. Next Pass

**Pass 9 — Domain Rules & Applicability Engine**

The next pass should define the actual deterministic rules that operate over this schema.

Focus areas:
- HS classification states
- requirement applicability
- temporal validity
- origin/destination rules
- agreement applicability
- preference eligibility
- tariff selection
- NTM applicability
- evidence sufficiency
- conflicting sources
- unresolved cases
- rule precedence.

The goal will be to define the platform's **business/domain logic formally enough that the AI layer can reason around it without replacing it**.