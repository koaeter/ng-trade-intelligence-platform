# Pass 81 — Source acquisition provenance

## Objective

Connect a registered source to an auditable acquisition attempt and, when successful, to the captured artifact.

## Model

Authority -> AuthorityEndpoint -> Source -> AcquisitionEvent -> SourceArtifact

An acquisition event is persisted for both successful and failed attempts. Failed attempts have no artifact, preserving an operational audit trail.

## Recorded provenance

Each event records source/endpoint identity, requested and retrieved URL, timestamps, outcome, HTTP status when available, content type and byte length, response SHA-256, user-agent identity, and a bounded error code/message.

Credentials, cookies, authorization headers, and response bodies are not persisted in the event.

## Boundary

Acquisition provenance is operational provenance, not regulatory authority. Successful retrieval does not publish a source, provision, or requirement.

The artifact keeps its own checksum because it proves the bytes persisted to object storage. The acquisition event checksum proves the bytes returned by the fetch operation.

## Lifecycle

Successful ingestion preserves the existing DISCOVERED -> ACQUIRED transition. Failed acquisition does not advance the source.

## Security

The HTTP adapter still requires HTTPS, an explicit host allowlist, bounded responses, timeouts, no URL credentials, and no automatic redirects. Complete SSRF defense remains a deployment/network responsibility, including DNS/IP egress controls.
