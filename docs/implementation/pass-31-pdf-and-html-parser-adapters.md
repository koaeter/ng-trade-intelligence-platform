# Pass 31 — PDF and HTML Parser Adapters

## Objective

Replace the placeholder extraction boundary with real, infrastructure-level parser adapters for PDF and HTML while keeping parser dependencies outside the domain and application layers.

## Implemented

### PDF

infrastructure/document_processing/pdf.py provides a PypdfDocumentExtractor using the existing pypdf dependency.

It:
- accepts only PDF artifacts;
- reads through the configured input bound;
- parses in strict mode;
- enforces max_pages;
- enforces max_output_characters;
- reports document page count;
- preserves page-aware extraction fragments with page_number and locator;
- records that OCR was not used;
- converts parser failures into controlled extraction errors.

The adapter does not execute embedded content and does not provide OCR. Scanned/image-only PDFs therefore remain a later OCR concern.

### HTML

infrastructure/document_processing/html.py provides a standard-library HTML parser.

It:
- accepts HTML artifacts;
- decodes UTF-8 only;
- extracts visible text;
- removes script, style, noscript, and template content;
- preserves the document title and heading levels as fragment metadata;
- enforces input and output bounds;
- performs no JavaScript execution;
- performs no network fetching.

The parser is intentionally local and non-executing. It is not a browser renderer.

## Application boundary refinement

DocumentExtractor.extract now receives the SourceArtifact explicitly. This makes parser results responsible for their own artifact identity and avoids the application service silently rewriting parser metadata.

The application service still owns:
- extractor selection;
- object-storage access;
- policy injection;
- lifecycle advancement;
- conversion to domain ExtractedText;
- conversion to stable ExtractionSegment records.

## Security and failure behaviour

Parser input remains untrusted.

The extraction layer fails closed when:
- input exceeds the configured byte bound;
- output exceeds the configured character bound;
- PDF page count exceeds the configured limit;
- UTF-8 decoding fails;
- a PDF cannot be parsed safely;
- a PDF page cannot be extracted.

No HTML scripts, macros, or active content are executed.

## Tests

The pass adds coverage for:
- multi-page PDF extraction;
- PDF page limits;
- PDF output limits;
- HTML script/style removal;
- HTML output limits;
- adapter routing through the application extraction service.

## Deliberate non-goals

This pass does not add:
- OCR;
- DOCX extraction;
- XLSX extraction;
- browser rendering;
- remote URL fetching from HTML;
- antivirus integration;
- candidate provision extraction;
- semantic chunking.

Those remain separate boundaries so parser behaviour does not become authoritative regulatory knowledge by itself.

## Resulting flow

Validated SourceArtifact -> Object Storage -> ExtractedTextService -> PDF/HTML Adapter -> Bounded ExtractionResult -> ExtractionSegment -> review/knowledge processing

The next logical pass is Pass 32 — extraction persistence and candidate provision segmentation, including page/section-aware extraction records and a controlled transition from extracted text to reviewable candidate provisions.
