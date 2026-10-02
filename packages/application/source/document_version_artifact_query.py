from packages.application.source.artifact_repositories import SourceArtifactRepository
from packages.domain.source.artifacts import SourceArtifact


class ListSourceArtifactsForDocumentVersion:
    """List immutable artifacts attached to one document version."""

    def __init__(self, artifacts: SourceArtifactRepository) -> None:
        self.artifacts = artifacts

    def execute(self, document_version_id: str) -> list[SourceArtifact]:
        return list(self.artifacts.list_for_document_version(document_version_id))