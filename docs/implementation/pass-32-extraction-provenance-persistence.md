# Pass 32 — Extraction provenance persistence

## Objective

Persist extraction fragments with stable source-location metadata so downstream provision extraction, evidence generation, and review can point back to the exact document location without treating extracted text as authoritative.

## Design

- ExtractedText remains the bounded aggregate extraction result.
- ExtractionSegment stores ordered fragments produced by an extractor.
- A segment belongs to exactly one SourceArtifact.
- sequence provides deterministic ordering.
- page_number, section, and locator preserve document-local location where available.
- source_start and source_end preserve offsets when available.
- Segments are provenance metadata, not legal provisions.
- The original artifact remains the authoritative binary source.
- Extracted text remains untrusted derived content.

## Persistence

Migration 0007 adds extraction_segments with a unique (artifact_id, sequence) constraint and indexes for artifact and page lookup.

Page number is optional because HTML, CSV, and plain text do not have pages.

## Deferred

Parser-specific production adapters, OCR implementations, and format-specific location strategies remain behind the extraction boundary. This pass establishes their durable persistence contract.
