from packages.application.scenarios.repositories import ExportScenarioRepository
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ApplicabilityEvaluation, EvaluationResult, ExportScenario


def create_scenario(repository: ExportScenarioRepository, scenario: ExportScenario) -> ExportScenario:
    repository.add(scenario)
    return scenario


def get_scenario(repository: ExportScenarioRepository, scenario_id: str) -> ExportScenario | None:
    return repository.get(scenario_id)


def evaluate_requirement(scenario: ExportScenario, requirement: Requirement) -> ApplicabilityEvaluation:
    result = EvaluationResult.APPLICABLE if requirement.is_effective_on(scenario.scenario_date) else EvaluationResult.NOT_APPLICABLE
    return ApplicabilityEvaluation(scenario.id, result, "initial")
