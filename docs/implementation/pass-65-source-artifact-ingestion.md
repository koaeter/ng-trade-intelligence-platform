# Pass 65 — Source acquisition to artifact ingestion

## Objective

Connect the external source fetch boundary to the existing SourceArtifact acquisition and object-storage model.

## Implemented

A successful source response now flows through:
- source fetch
- artifact acquisition policy
- content validation
- SHA-256 checksum
- object storage
- SourceArtifact creation
- artifact repository persistence

The artifact records source/document identity, storage key, checksum, acquisition time and normalized MIME type.

## Authority boundary

Successful HTTP retrieval does not publish regulatory knowledge. It only creates an acquired artifact. Extraction, review and publication remain separate lifecycle stages.

## Next

The next pass should add source/document lifecycle transitions around acquisition and extraction so the source registry reflects processing state without conflating acquisition with legal publication.
