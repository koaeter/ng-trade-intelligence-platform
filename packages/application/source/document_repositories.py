from abc import ABC, abstractmethod

from packages.domain.source.models import Document


class DocumentRepository(ABC):
    @abstractmethod
    def add(self, document: Document) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, document_id: str) -> Document | None:
        raise NotImplementedError
