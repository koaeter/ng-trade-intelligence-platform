from packages.application.source.document_repositories import DocumentRepository
from packages.application.source.document_version_repositories import DocumentVersionRepository
from packages.domain.source.document_versions import DocumentVersion


class RegisterDocumentVersion:
    def __init__(
        self,
        versions: DocumentVersionRepository,
        documents: DocumentRepository,
    ) -> None:
        self.versions = versions
        self.documents = documents

    def execute(self, version: DocumentVersion) -> DocumentVersion:
        if self.documents.get(version.document_id) is None:
            raise ValueError("Document version must reference an existing document")
        if self.versions.get(version.id) is not None:
            raise ValueError("Document version already exists")
        if version.effective_to is not None and version.effective_from is not None:
            if version.effective_to <= version.effective_from:
                raise ValueError("Document version effective_to must be after effective_from")
        if version.version_label is not None and not version.version_label.strip():
            raise ValueError("Document version label cannot be blank")
        self.versions.add(version)
        return version
