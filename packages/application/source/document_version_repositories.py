from abc import ABC, abstractmethod

from packages.domain.source.document_versions import DocumentVersion


class DocumentVersionRepository(ABC):
    @abstractmethod
    def add(self, version: DocumentVersion) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, version_id: str) -> DocumentVersion | None:
        raise NotImplementedError

    @abstractmethod
    def list_for_document(self, document_id: str, limit: int | None = None) -> list[DocumentVersion]:
        raise NotImplementedError
