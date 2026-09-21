from abc import ABC, abstractmethod

from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ApplicabilityEvaluation, ExportScenario


class ExportScenarioRepository(ABC):
    @abstractmethod
    def add(self, scenario: ExportScenario) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, scenario_id: str) -> ExportScenario | None:
        raise NotImplementedError


class RequirementRepository(ABC):
    @abstractmethod
    def add(self, requirement: Requirement) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, requirement_id: str) -> Requirement | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Requirement]:
        raise NotImplementedError


class ApplicabilityEvaluationRepository(ABC):
    @abstractmethod
    def add(self, evaluation: ApplicabilityEvaluation) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_for_scenario(self, scenario_id: str) -> list[ApplicabilityEvaluation]:
        raise NotImplementedError
