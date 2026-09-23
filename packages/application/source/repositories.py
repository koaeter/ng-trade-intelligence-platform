from abc import ABC, abstractmethod

from packages.domain.source.models import Document, Provision, Source


class SourceRepository(ABC):
    @abstractmethod
    def add(self, source: Source) -> None: raise NotImplementedError
    @abstractmethod
    def get(self, source_id: str) -> Source | None: raise NotImplementedError
    @abstractmethod
    def update(self, source: Source) -> None: raise NotImplementedError


class DocumentRepository(ABC):
    @abstractmethod
    def add(self, document: Document) -> None: raise NotImplementedError
    @abstractmethod
    def get(self, document_id: str) -> Document | None: raise NotImplementedError


class ProvisionRepository(ABC):
    @abstractmethod
    def add(self, provision: Provision) -> None: raise NotImplementedError
    @abstractmethod
    def get(self, provision_id: str) -> Provision | None: raise NotImplementedError
