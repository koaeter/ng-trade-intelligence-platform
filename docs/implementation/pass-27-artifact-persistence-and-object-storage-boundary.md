# Pass 27 — Artifact Persistence & Object-Storage Boundary

## Objective

Give the document-artifact and extraction concepts introduced in Pass 26 durable persistence while keeping binary content outside the relational database.

## Persistence model

```text
Source
  ↓
Document
  ↓
SourceArtifact
  ├── metadata → PostgreSQL
  └── binary content → Object Storage
          ↓
      storage_key
          ↓
     ExtractedText → PostgreSQL
```

### Source artifacts

The relational record stores artifact identity, source/document ownership, artifact kind, provider-neutral `storage_key`, SHA-256 checksum, acquisition timestamp, MIME type, original filename, and processing state.

The binary itself is deliberately not stored in PostgreSQL.

### Extracted text

Each artifact has at most one current extracted-text record in this first persistence boundary. It stores the artifact ID, extracted text, extractor name/version, extraction timestamp, and OCR-used flag.

## Object-storage boundary

`ObjectStorage` is an application-facing port with `put`, `get`, and `delete`.

No S3, Azure Blob, MinIO, Google Cloud Storage, or other provider SDK is part of the application/domain layer.

The `storage_key` is an opaque application identifier. The domain does not interpret it as a provider-specific URI.

## Integrity

The SHA-256 checksum is stored with artifact metadata so acquisition can later verify that the retrieved object is the same artifact that was registered.

A checksum is indexed for lookup, but is not globally unique: the same binary may legitimately occur in more than one source/document context.

## Foreign-key boundary

An artifact belongs to an existing source and document. Extracted text is dependent on its artifact and is removed when that artifact is removed at the database level.

## Not implemented yet

- S3-compatible implementation;
- object download/upload API endpoints;
- malware scanning;
- MIME/content sniffing;
- size limits;
- retention policies;
- artifact version/deduplication workflow;
- PDF/HTML/DOCX extraction;
- OCR;
- chunking/page coordinates.

Those remain infrastructure or later knowledge-processing passes.
