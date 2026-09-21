from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import (
    ApplicabilityEvaluation,
    EvaluationResult,
    ExportScenario,
)


def evaluate_requirement(
    scenario: ExportScenario,
    requirement: Requirement,
) -> ApplicabilityEvaluation:
    if requirement.is_effective_on(scenario.scenario_date):
        result = EvaluationResult.APPLICABLE
    else:
        result = EvaluationResult.NOT_APPLICABLE

    return ApplicabilityEvaluation(
        scenario_id=scenario.id,
        result=result,
        rule_set_version="initial",
    )
