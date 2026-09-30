from abc import ABC, abstractmethod

from packages.domain.source.document_relationships import DocumentRelationship


class DocumentRelationshipRepository(ABC):
    @abstractmethod
    def add(self, relationship: DocumentRelationship) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, relationship_id: str) -> DocumentRelationship | None:
        raise NotImplementedError

    @abstractmethod
    def list_for_version(self, version_id: str) -> list[DocumentRelationship]:
        raise NotImplementedError
