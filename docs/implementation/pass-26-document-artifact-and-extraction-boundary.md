# Pass 26 — Document Artifact & Extraction Boundary

## Objective

Introduce the first explicit boundary between an authoritative source/document and the physical or retrieved artifact used to extract text from it.

## New concepts

### Source artifact

A source artifact represents the acquired representation of a document:

~~~text
Source
  ↓
Document
  ↓
SourceArtifact
  ↓
ExtractedText
~~~

The artifact records source/document ownership, artifact kind, storage key, SHA-256 checksum, acquisition timestamp, MIME type/original filename, and processing state.

### Extracted text

Extracted text records its originating artifact, extracted text, extractor identity/version, extraction timestamp, and whether OCR was used.

Extracted text is **not authoritative knowledge**.

The authoritative chain remains:

~~~text
Source
  ↓
Document
  ↓
Provision
  ↓
Evidence
  ↓
Published Requirement
~~~

The extraction path is supporting infrastructure:

~~~text
SourceArtifact
  ↓
ExtractedText
  ↓
Candidate Provisions
  ↓
Human / governance review
  ↓
Published Provisions
~~~

## Design decision

The system does not yet store binary files in PostgreSQL. The storage_key field deliberately acts as the object-storage boundary. A later infrastructure pass will provide an S3-compatible adapter and object lifecycle policy.

## Security

Acquired artifacts and extracted text are untrusted input. They must not be treated as instructions by an AI system. File validation, malware scanning, size/type limits and sandboxed extraction belong in acquisition infrastructure.

## Not implemented yet

- object-storage adapter;
- PDF/HTML/DOCX extraction implementation;
- OCR engine;
- page/section coordinates;
- document chunking;
- artifact database persistence;
- candidate provision generation.

Those will be introduced incrementally rather than hidden inside the domain model.
