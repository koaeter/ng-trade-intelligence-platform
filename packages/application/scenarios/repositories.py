from abc import ABC, abstractmethod
from packages.domain.scenario.models import ExportScenario


class ExportScenarioRepository(ABC):
    @abstractmethod
    def add(self, scenario: ExportScenario) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, scenario_id: str) -> ExportScenario | None:
        raise NotImplementedError
