from abc import ABC, abstractmethod

from packages.domain.source.acquisition import AcquisitionEvent


class AcquisitionEventRepository(ABC):
    @abstractmethod
    def add(self, event: AcquisitionEvent) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, event_id: str) -> AcquisitionEvent | None:
        raise NotImplementedError

    @abstractmethod
    def link_artifact(self, event_id: str, artifact_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_for_source(self, source_id: str) -> list[AcquisitionEvent]:
        raise NotImplementedError
