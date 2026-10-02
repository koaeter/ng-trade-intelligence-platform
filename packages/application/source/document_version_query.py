from packages.application.source.document_version_repositories import DocumentVersionRepository
from packages.domain.source.document_versions import DocumentVersion


class GetDocumentVersion:
    """Read one immutable document version."""

    def __init__(self, versions: DocumentVersionRepository) -> None:
        self.versions = versions

    def execute(self, version_id: str) -> DocumentVersion:
        version = self.versions.get(version_id)
        if version is None:
            raise ValueError("Document version does not exist")
        return version


class ListDocumentVersions:
    """List immutable versions belonging to one document."""

    def __init__(self, versions: DocumentVersionRepository) -> None:
        self.versions = versions

    def execute(self, document_id: str) -> list[DocumentVersion]:
        return list(self.versions.list_for_document(document_id))
