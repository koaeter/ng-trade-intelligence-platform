from datetime import date

from packages.application.scenarios.services import evaluate_requirement, evaluate_scenario
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import EvaluationResult, ExportScenario


def scenario() -> ExportScenario:
    return ExportScenario("scenario-1", "product-1", "1801", "NG", "DE", date(2026, 9, 21))


def test_active_requirement_is_applicable() -> None:
    result = evaluate_requirement(scenario(), Requirement("req-1", "Sample", date(2026, 1, 1)))
    assert result.result == EvaluationResult.APPLICABLE
    assert result.scenario_id == "scenario-1"


def test_expired_requirement_is_not_applicable() -> None:
    result = evaluate_requirement(scenario(), Requirement("req-1", "Sample", date(2025, 1, 1), date(2026, 9, 20)))
    assert result.result == EvaluationResult.NOT_APPLICABLE


def test_evaluate_scenario_persists_each_requirement() -> None:
    class Scenarios:
        def get(self, scenario_id: str) -> ExportScenario | None:
            return scenario() if scenario_id == "scenario-1" else None
    class Requirements:
        def list_all(self) -> list[Requirement]:
            return [Requirement("req-1", "Active", date(2026, 1, 1)), Requirement("req-2", "Future", date(2027, 1, 1))]
    class Evaluations:
        def __init__(self) -> None:
            self.items: list[object] = []
        def add(self, evaluation: object) -> None:
            self.items.append(evaluation)
    evaluations = Evaluations()
    result = evaluate_scenario(Scenarios(), Requirements(), evaluations, "scenario-1")  # type: ignore[arg-type]
    assert [x.result for x in result] == [EvaluationResult.APPLICABLE, EvaluationResult.NOT_APPLICABLE]
    assert len(evaluations.items) == 2
