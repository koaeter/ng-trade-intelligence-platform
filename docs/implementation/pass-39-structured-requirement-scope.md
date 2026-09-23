# Pass 39 — Structured requirement scope candidates

## Objective

Introduce a structured, reviewable scope representation before a Requirement becomes authoritative.

## Implemented

A RequirementScopeCandidate can capture:
- products
- HS version/code pairs
- origin countries
- destination markets
- effective dates
- textual conditions requiring later rule structuring

The scope is normalized and validated, but it is still attached to a RequirementCandidate and is not itself an authoritative applicability rule.

## Design principle

The platform must not force legal applicability into a free-text field.

The candidate pipeline now has a place to capture:

Requirement text
  +
structured scope
  +
conditions
  +
source provision

before deterministic evaluation rules are published.

## Unresolved information

Empty scope is allowed because the provision may not explicitly state all applicability dimensions. Missing scope must remain missing; it is not inferred to mean "all".

## Next

The next pass should add review governance for RequirementCandidate and RequirementScopeCandidate so publication requires explicit scope review and evidence.
