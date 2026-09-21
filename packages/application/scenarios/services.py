from packages.application.scenarios.repositories import (
    ApplicabilityEvaluationRepository,
    ExportScenarioRepository,
    RequirementRepository,
)
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ApplicabilityEvaluation, EvaluationResult, ExportScenario


RULE_SET_VERSION = "initial"


def create_scenario(repository: ExportScenarioRepository, scenario: ExportScenario) -> ExportScenario:
    repository.add(scenario)
    return scenario


def get_scenario(repository: ExportScenarioRepository, scenario_id: str) -> ExportScenario | None:
    return repository.get(scenario_id)


def evaluate_requirement(scenario: ExportScenario, requirement: Requirement) -> ApplicabilityEvaluation:
    result = EvaluationResult.APPLICABLE if requirement.is_effective_on(scenario.scenario_date) else EvaluationResult.NOT_APPLICABLE
    return ApplicabilityEvaluation(scenario.id, result, RULE_SET_VERSION)


def evaluate_scenario(
    scenario_repository: ExportScenarioRepository,
    requirement_repository: RequirementRepository,
    evaluation_repository: ApplicabilityEvaluationRepository,
    scenario_id: str,
) -> list[ApplicabilityEvaluation]:
    scenario = scenario_repository.get(scenario_id)
    if scenario is None:
        raise ValueError(f"Export scenario not found: {scenario_id}")

    evaluations = [evaluate_requirement(scenario, requirement) for requirement in requirement_repository.list_all()]
    for evaluation in evaluations:
        evaluation_repository.add(evaluation)
    return evaluations
