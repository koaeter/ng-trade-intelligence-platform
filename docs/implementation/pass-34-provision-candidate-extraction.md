# Pass 34 — Provision candidate extraction

## Objective

Create the first governed bridge between extracted document fragments and regulatory knowledge without promoting extracted text directly into authoritative provisions.

## Implemented

- Added ProvisionCandidate as a separate domain object.
- Added an explicit candidate lifecycle: EXTRACTED, REVIEWED, ACCEPTED, REJECTED.
- Added a candidate repository boundary.
- Added persistence for candidates with links to document, artifact, and exact extraction segment.
- Added deterministic candidate extraction that creates one reviewable candidate per non-empty extraction segment.
- Preserved the extraction locator as the candidate's evidence location.
- Kept candidate classification as UNCLASSIFIED until a later review/classification stage.

## Provenance chain

Source
  -> Document
  -> SourceArtifact
  -> ExtractionSegment
  -> ProvisionCandidate
  -> later reviewed Provision

The candidate is not a Provision. The distinction is intentional: extraction can be wrong, incomplete, or structurally ambiguous.

## What this pass does not do

- It does not infer legal meaning.
- It does not classify a candidate as a requirement, prohibition, definition, tariff rule, exception, or other legal type.
- It does not publish candidate text.
- It does not use an LLM to create authoritative knowledge.

## Next

The next pass should add candidate review/classification infrastructure so a human-governed process can transform selected candidates into authoritative Provision records while preserving the original extraction provenance.
