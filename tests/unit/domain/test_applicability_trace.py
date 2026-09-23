from datetime import date

from packages.domain.requirement.evaluation import TruthValue
from packages.domain.scenario.applicability_trace import ApplicabilityTrace
from packages.domain.scenario.models import EvaluationResult


def test_applicability_trace_is_reproducible_data():
    trace = ApplicabilityTrace(
        "scenario-1", "requirement-1", date(2026, 9, 21),
        TruthValue.TRUE, TruthValue.TRUE, TruthValue.TRUE,
        EvaluationResult.APPLICABLE, EvaluationResult.APPLICABLE,
    )
    assert trace.scenario_id == "scenario-1"
    assert trace.final_result == EvaluationResult.APPLICABLE
