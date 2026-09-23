# Pass 29 — Document Content Validation & Secure Processing

## Objective

Prevent unvalidated or potentially malicious source artifacts from crossing the object-storage boundary.

## Implemented

- Added provider-neutral content inspection in \`packages/application/source/content_validation.py\`.
- Added signature detection for PDF, PNG, JPEG and ZIP containers.
- Added explicit text/HTML handling; text formats are not treated as having a reliable binary magic signature.
- Added declared MIME versus detected-format consistency checks.
- Added a \`MalwareScanner\` protocol with CLEAN, INFECTED, UNAVAILABLE and ERROR states.
- Added a development-only no-op scanner that reports UNAVAILABLE rather than pretending content is safe.
- Integrated validation into \`ArtifactAcquisitionService\`, so failed content validation or malware scanning prevents object storage.
- Added tests for valid formats, Office ZIP containers, MIME mismatch, infection, unavailable/error scanner states, unknown content and no-storage-on-failure.

## Security boundary

\`\`\`
Acquisition Adapter
      ↓
Bounded Read / Size Limit
      ↓
Content Validation
 ├── Signature Inspection
 ├── Declared MIME Consistency
 └── Malware Scanner Port
      ↓
ACCEPTED ─────────→ Object Storage
      ↓
SourceArtifact
\`\`\`

The acquisition layer treats source bytes as untrusted data and never executes uploaded content.

## MIME and signature policy

A detected format is not inferred from a filename extension. The validator inspects content signatures where reliable:

- PDF begins with the PDF signature.
- PNG uses its standard eight-byte signature.
- JPEG uses its standard image signature.
- DOCX/XLSX are recognised only as ZIP containers at this pass.
- Text, HTML and CSV are handled as UTF-8 text-like content.

A ZIP signature alone does not prove that the package is a valid DOCX or XLSX document. Package-level validation is deferred to document processing.

## Malware scanning boundary

The application depends on a provider-neutral scanner interface. A real scanner can later be implemented using an isolated antivirus service without changing the domain/application contract.

The default development scanner returns \`UNAVAILABLE\`. This is deliberately fail-closed: an unavailable scanner does not cause content to be accepted.

## Important limitations

This pass does not yet provide:

- a real ClamAV or other malware-scanning adapter;
- archive bomb detection;
- DOCX/XLSX package validation;
- PDF parser hardening;
- HTML sanitisation;
- sandboxed document extraction;
- page/section coordinates;
- extraction workers.

Those belong to subsequent secure-processing passes.

## Next

Pass 30 should establish the extraction-worker boundary and safe PDF/HTML/DOCX/XLSX text-extraction pipeline, including parser resource limits, sandboxing, extraction metadata and page/section provenance.
