# Pass 30 — Secure Document Extraction Boundary

## Objective

Establish a safe extraction-worker boundary without making document parsers part of the domain model.

## Implemented

- Added a provider-neutral DocumentExtractor port.
- Added bounded extraction policy for output size and future page limits.
- Added ExtractedTextService, which retrieves an already-validated artifact from object storage and selects an extractor by governed ArtifactKind.
- Added a UTF-8 text/HTML/CSV extractor as the first concrete implementation.
- Added extraction metadata: extractor name/version, OCR usage and optional page count.
- Added tests for successful extraction, output limits, unsupported formats and invalid UTF-8.
- Kept PDF/DOCX/XLSX parser implementations out of the application layer.

## Processing boundary

Validated SourceArtifact
        |
        v
Object Storage
        |
        v
Extraction Worker / Service
        |
        v
DocumentExtractor
        |
        v
Bounded ExtractedText
        |
        v
Extraction Metadata
        |
        v
Candidate Provision Processing

## Security rules

Extractors receive untrusted bytes and must not execute document content. Parser-specific resource limits belong to each infrastructure adapter. Extraction output is not authoritative legal knowledge.

The application layer controls the contract and limits; infrastructure adapters will implement PDF, DOCX and XLSX parsing later.

## Current limitation

This pass deliberately does not pretend that a PDF, DOCX or XLSX parser exists. Those formats currently fail with "No extractor registered". This is safer than silently decoding arbitrary binary content as text.

## Next

Pass 31 should add production-oriented parser adapters behind this boundary, beginning with PDF and HTML, including sanitisation/resource limits and location-aware extraction metadata. DOCX/XLSX can follow behind the same interface.
