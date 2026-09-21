from datetime import date

from packages.application.scenarios.services import evaluate_requirement
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import EvaluationResult, ExportScenario


def test_active_requirement_is_applicable() -> None:
    scenario = ExportScenario(
        id="scenario-1",
        product_id="product-1",
        hs_code="1801",
        origin_country_code="NG",
        destination_market_code="DE",
        scenario_date=date(2026, 9, 21),
    )
    requirement = Requirement(
        id="req-1",
        name="Sample requirement",
        effective_from=date(2026, 1, 1),
    )

    result = evaluate_requirement(scenario, requirement)

    assert result.result == EvaluationResult.APPLICABLE
    assert result.scenario_id == "scenario-1"
