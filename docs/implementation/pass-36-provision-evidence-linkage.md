# Pass 36 — Provision evidence linkage

## Objective

Ensure accepted regulatory provisions have a direct, queryable evidence record pointing back to the exact extraction segment from which the reviewed text originated.

## Implemented

- Added a provision evidence service.
- Resolves the authoritative source through the provision's document.
- Creates a verified regulatory-provision Evidence record after review.
- Preserves the extraction segment identifier and document-local locator.
- Preserves the candidate text as the evidence excerpt.
- Prevents attaching evidence when the candidate and provision belong to different documents.

## Provenance chain

Finding
  -> Evidence
  -> Provision
  -> Document
  -> Source

And for extracted regulatory text:

Provision
  -> Evidence locator
  -> ExtractionSegment
  -> SourceArtifact
  -> Document
  -> Source

The binary artifact remains the original source representation. Extracted text remains derived.

## Next

The next pass should introduce a controlled provision-type vocabulary and validation so accepted provisions cannot carry arbitrary ungoverned semantic types.
