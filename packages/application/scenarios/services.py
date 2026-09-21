from packages.application.scenarios.repositories import (
    ApplicabilityEvaluationRepository,
    EvidenceRepository,
    ExportScenarioRepository,
    RequirementRepository,
)
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ApplicabilityEvaluation, EvaluationResult, ExportScenario


RULE_SET_VERSION = "initial"


def create_scenario(repository: ExportScenarioRepository, scenario: ExportScenario) -> ExportScenario:
    repository.add(scenario)
    return scenario


def get_scenario(repository: ExportScenarioRepository, scenario_id: str) -> ExportScenario | None:
    return repository.get(scenario_id)


def evaluate_requirement(
    scenario: ExportScenario,
    requirement: Requirement,
    evidence: tuple[Evidence, ...] = (),
) -> ApplicabilityEvaluation:
    if not requirement.is_effective_on(scenario.scenario_date):
        result = EvaluationResult.NOT_APPLICABLE
    else:
        scope = requirement.scope_matches(
            scenario.product_id,
            scenario.hs_code,
            scenario.origin_country_code,
            scenario.destination_market_code,
        )
        if scope is False:
            result = EvaluationResult.NOT_APPLICABLE
        elif not evidence:
            result = EvaluationResult.INSUFFICIENT_EVIDENCE
        elif not all(item.verified for item in evidence):
            result = EvaluationResult.UNRESOLVED
        else:
            result = EvaluationResult.APPLICABLE

    return ApplicabilityEvaluation(
        scenario.id,
        requirement.id,
        result,
        RULE_SET_VERSION,
        evidence,
    )


def evaluate_scenario(
    scenario_repository: ExportScenarioRepository,
    requirement_repository: RequirementRepository,
    evaluation_repository: ApplicabilityEvaluationRepository,
    evidence_repository: EvidenceRepository,
    scenario_id: str,
) -> list[ApplicabilityEvaluation]:
    scenario = scenario_repository.get(scenario_id)
    if scenario is None:
        raise ValueError(f"Export scenario not found: {scenario_id}")

    evaluations = []
    for requirement in requirement_repository.list_all():
        evidence = tuple(
            item for evidence_id in requirement.evidence_ids
            if (item := evidence_repository.get(evidence_id)) is not None
        )
        evaluations.append(evaluate_requirement(scenario, requirement, evidence))

    for evaluation in evaluations:
        evaluation_repository.add(evaluation)
    return evaluations
