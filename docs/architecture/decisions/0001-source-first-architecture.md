# ADR 0001: Source-First Architecture

## Status

Accepted — initial architectural principle.

## Decision

Authoritative documents and structured datasets are treated as primary sources. AI-generated output is derived from retrieved evidence rather than being treated as the authoritative record.

## Rationale

The platform is intended for regulatory and trade intelligence use. Users need to be able to trace substantive answers back to source material and understand the temporal validity and status of the underlying information.

## Consequences

- Documents require provenance and versioning.
- Regulatory instruments need effective/status metadata.
- Retrieval results should retain source references.
- AI responses should expose supporting evidence where appropriate.
- Conflicting or superseded sources must not silently overwrite historical information.
