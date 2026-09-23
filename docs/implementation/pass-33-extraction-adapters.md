# Pass 33 — Actual extraction adapters

## Objective

Replace the placeholder format boundary with concrete, bounded adapters while keeping parser-specific code outside the application/domain layers.

## Implemented

- HTML extraction with active-content sanitisation. Script/style/template/SVG/canvas content is excluded from extracted text.
- PDF extraction through the pypdf adapter, preserving page boundaries and page locators.
- DOCX extraction through the Office Open XML package directly, preserving paragraph order.
- XLSX extraction through the Office Open XML package directly, preserving sheet and row locators.
- ZIP/container limits for Office formats: member count, individual uncompressed member size, aggregate uncompressed size, and path traversal checks.
- A shared extraction input limit and output-character limit.
- Extraction fragments are converted into persisted-domain ExtractionSegment values by the application service.
- Parser failures are surfaced as extraction failures rather than silently returning untrusted binary data.

## Architecture

SourceArtifact
  -> ObjectStorage
  -> ExtractedTextService
  -> DocumentExtractor
  -> format-specific infrastructure adapter
  -> bounded ExtractionResult
  -> ExtractionSegment
  -> later provision extraction/review

## Dependency

PDF extraction uses pypdf. The application/domain contracts do not import it.

## Deliberate limits

- This pass does not add OCR.
- This pass does not classify legal provisions.
- This pass does not treat extracted text as authoritative.
- XLSX formula evaluation is not performed; cached cell values are read where available.
- PDF extraction quality depends on the source PDF's text layer. Scanned-image PDFs remain an OCR concern.
