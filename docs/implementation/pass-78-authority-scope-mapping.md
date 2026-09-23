# Pass 78 — Authority to Regulatory Scope Mapping

## Purpose

Pass 78 makes the Nigerian authority registry operational by declaring the regulatory domains and fact types for which each registered authority is a candidate source.

The mapping is deliberately not a legal-precedence table. It answers:

> Which authorities should be considered for this jurisdiction/domain/fact-type combination?

Precedence remains a separate, source-specific concern handled by SourceAuthorityAssignment and deterministic authority resolution.

## Model

    Authority
       + Jurisdiction
       + Regulatory Domain Code
       + Fact Type Code
       |
       v
    AuthorityScopeAssignment

The assignment is intentionally code-based for domain and fact type. This lets the authority registry be established before the full domain/fact-type master-data seed is populated, while preserving a stable contract for later resolution against those registries.

## Initial Nigerian scope

The seed covers:

- NEPC — export documentation, procedures and market-access support
- NCS — customs procedures and tariff administration
- SON — standards and conformity
- NAFDAC — SPS/product-regulation controls, certification and procedures
- NAQS — phytosanitary SPS controls and certification
- DVPCS — veterinary SPS controls and certification
- Department of Fisheries — fisheries SPS controls and certification
- NiNAS — accreditation/conformity infrastructure

The mapping reflects the current NEPC description of Nigerian quality competent authorities and export documentation. NEPC identifies NAFDAC, NAQS, DVPCS and Fisheries for specific export certificates, and identifies SON and NiNAS in standards/accreditation roles.

## Important boundary

A scope assignment does not establish that every fact published by an authority is legally binding. Legal effect, source authority, temporal validity, verification status and precedence remain separate fields and decisions.

## Next dependency

The next pass can populate authoritative source endpoints and source records using these scope mappings as the classification layer.
