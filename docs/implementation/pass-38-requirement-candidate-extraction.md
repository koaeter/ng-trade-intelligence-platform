# Pass 38 — Requirement candidate extraction

## Objective

Create a governed candidate layer between accepted regulatory provisions and authoritative Requirement records.

## Implemented

- Added RequirementCandidate with an explicit lifecycle.
- Added a repository boundary and persistence.
- Added deterministic candidate creation from accepted Provision records.
- Preserved the originating provision and document.
- Generated only a proposed human-readable name; no applicability scope is inferred.

## Governance boundary

The pipeline is now:

Source
  -> Document
  -> Artifact
  -> ExtractionSegment
  -> ProvisionCandidate
  -> reviewed Provision
  -> RequirementCandidate
  -> later structured Requirement

The RequirementCandidate is not an authoritative Requirement.

## Important limitation

A sentence that contains words such as "must", "shall", or "required" is not automatically enough to determine the legal scope of a requirement. Product, HS code, origin, destination, date, exceptions and conditions must be structured from evidence before publication.

## Next

The next pass should add structured requirement-scope candidates so review can capture product, HS, origin, destination and temporal applicability without yet publishing a deterministic rule.
