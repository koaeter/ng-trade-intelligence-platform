# Pass 28 — Secure Artifact Acquisition & Object Storage

## Objective

Turn the storage boundary into a controlled acquisition boundary without coupling the domain to a specific object-storage provider.

## Acquisition flow

```text
External Source
      ↓
Acquisition Adapter
      ↓
Artifact Acquisition Policy
 ├── storage-key validation
 ├── MIME allowlist
 ├── bounded size
 └── SHA-256 checksum
      ↓
ObjectStorage
      ↓
SourceArtifact metadata
```

The acquisition service operates on a binary stream and does not decide whether the document is authoritative. It only establishes a controlled artifact.

## Security boundary

This pass establishes:

- traversal-safe storage keys;
- configurable maximum artifact size;
- an explicit MIME-type allowlist;
- SHA-256 integrity calculation;
- provider-neutral object storage;
- a development-only local filesystem adapter.

The local adapter is intentionally an infrastructure implementation for development/testing. It is not the production storage recommendation.

## Important limitation

MIME type is supplied by the acquisition caller and is therefore **untrusted metadata**. It is not equivalent to content sniffing or malware scanning.

Future acquisition infrastructure must add:

1. content-signature/magic-byte validation;
2. malware scanning/quarantine;
3. decompression-bomb protection;
4. archive/member limits where archives are supported;
5. source-specific authentication and rate limiting;
6. object retention and lifecycle controls.

## Integrity model

The acquisition service calculates SHA-256 over the bytes it receives before storage. The checksum is an integrity identifier, not proof that the source itself is authoritative.

## Design boundary

```text
Application
    ↓
ObjectStorage port
    ↓
Infrastructure adapter
    ├── LocalObjectStorage (development)
    └── S3-compatible adapter (later)
```

No S3 SDK or provider-specific URI is introduced into the domain or application layers.
