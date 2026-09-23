from datetime import datetime, timezone
from uuid import uuid4

from packages.application.source.artifact_acquisition import ArtifactAcquisitionService
from packages.application.source.source_acquisition import AcquiredSourceResponse
from packages.domain.source.artifacts import ArtifactKind, SourceArtifact


class SourceIngestionService:
    def __init__(self, acquisition: ArtifactAcquisitionService, artifacts, sources) -> None:
        self.acquisition = acquisition
        self.artifacts = artifacts
        self.sources = sources

    def ingest(
        self,
        source_id: str,
        document_id: str,
        storage_key: str,
        response: AcquiredSourceResponse,
    ) -> SourceArtifact:
        artifact_id = str(uuid4())
        acquired = self.acquisition.acquire(
            storage_key,
            content=_bytes(response.body),
            content_type=response.content_type.split(";", 1)[0].strip().lower()
            if response.content_type
            else None,
        )
        mime = response.content_type.split(";", 1)[0].strip().lower() if response.content_type else None
        artifact = SourceArtifact(
            id=artifact_id,
            source_id=source_id,
            document_id=document_id,
            kind=_kind_for_mime(mime),
            storage_key=acquired.storage_key,
            checksum_sha256=acquired.checksum_sha256,
            acquired_at=datetime.now(timezone.utc),
            mime_type=mime,
        )
        self.artifacts.add(artifact)
        source = self.sources.get(source_id)
        if source is not None:
            from packages.application.source.lifecycle import SourceLifecycleService
            from packages.domain.source.models import SourceStatus
            if source.status == SourceStatus.DISCOVERED:
                self.sources.update(
                    SourceLifecycleService().transition(source, SourceStatus.ACQUIRED)
                )
        return artifact


def _bytes(value: bytes):
    from io import BytesIO
    return BytesIO(value)


def _kind_for_mime(mime: str | None) -> ArtifactKind:
    return {
        "application/pdf": ArtifactKind.PDF,
        "text/html": ArtifactKind.HTML,
        "text/plain": ArtifactKind.TEXT,
        "text/csv": ArtifactKind.CSV,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ArtifactKind.DOCX,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ArtifactKind.XLSX,
        "image/png": ArtifactKind.IMAGE,
        "image/jpeg": ArtifactKind.IMAGE,
    }.get(mime, ArtifactKind.OTHER)
