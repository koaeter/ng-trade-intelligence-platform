from dataclasses import dataclass

from packages.application.source.artifact_repositories import SourceArtifactRepository
from packages.application.source.document_version_repositories import (
    DocumentVersionRepository,
)
from packages.domain.source.artifacts import SourceArtifact
from packages.domain.source.document_versions import DocumentVersion


@dataclass(frozen=True)
class DocumentProvenance:
    versions: tuple[DocumentVersion, ...]
    artifacts_by_version: dict[str, tuple[SourceArtifact, ...]]


class GetDocumentProvenance:
    """Build a read-only document-version/artifact provenance view."""

    def __init__(
        self,
        versions: DocumentVersionRepository,
        artifacts: SourceArtifactRepository,
    ) -> None:
        self.versions = versions
        self.artifacts = artifacts

    def execute(self, document_id: str) -> DocumentProvenance:
        versions = tuple(self.versions.list_for_document(document_id))
        artifacts = {
            version.id: tuple(self.artifacts.list_for_document_version(version.id))
            for version in versions
        }
        return DocumentProvenance(
            versions=versions,
            artifacts_by_version=artifacts,
        )