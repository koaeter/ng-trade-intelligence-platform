# Pass 40 — Requirement publication governance

## Objective

Create an explicit publication boundary from a RequirementCandidate to the existing authoritative Requirement model.

## Implemented

Publication now requires:
- an existing RequirementCandidate
- a structured RequirementScopeCandidate
- explicit scope review
- a reviewer reference
- at least one evidence reference
- a valid effective period
- explicit confirmation when the structured scope is intentionally general
- successful resolution of every referenced product, HS code, country and market

The published Requirement receives only resolved structured entities and evidence identifiers.

## Important semantic rule

An empty scope is not silently treated as universal scope during publication.

The existing Requirement evaluator may use empty dimensions as wildcard semantics, so publication now requires explicit confirmation before an empty structured scope can enter the authoritative Requirement model.

## Pipeline

Provision
  -> RequirementCandidate
  -> RequirementScopeCandidate
  -> reviewed publication decision
  -> Requirement
  -> deterministic applicability engine

## Next

The next pass should introduce structured condition candidates so requirements that depend on quantity, value, exporter type, intended use or processing state can be represented without overloading product/country scope fields.
