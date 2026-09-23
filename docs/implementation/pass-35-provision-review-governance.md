# Pass 35 — Provision review governance

## Objective

Create an explicit governance boundary between extracted provision candidates and authoritative Provision records.

## Implemented

- Added a review decision object requiring a reviewer reference.
- Added persisted review history.
- Added candidate status transitions.
- Added an application service that only creates a Provision after an explicit ACCEPTED decision and provision type.
- Rejection is persisted without creating a Provision.
- REVIEWED decisions preserve the candidate for further processing.
- Accepted Provision records retain the candidate's document and locator.

## Governance rule

The following transition is explicit:

Extracted document
  -> ExtractionSegment
  -> ProvisionCandidate
  -> human review decision
  -> accepted Provision

The system does not infer that an extracted sentence is legally authoritative merely because it came from an official-looking document.

## Audit boundary

Review history records:
- candidate
- reviewer reference
- decision
- reason
- review timestamp

Authentication and authorization of the reviewer remain application/security concerns and are deliberately not embedded in this domain service.

## Next

The next pass should strengthen provision classification and evidence linkage so accepted provisions have structured types and direct, queryable provenance before regulatory requirements are derived from them.
