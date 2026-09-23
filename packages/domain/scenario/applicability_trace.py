from dataclasses import dataclass
from datetime import date

from packages.domain.requirement.evaluation import ConditionSetEvaluation, TruthValue
from packages.domain.scenario.models import EvaluationResult


@dataclass(frozen=True)
class ApplicabilityTrace:
    scenario_id: str
    requirement_id: str
    scenario_date: date
    temporal_result: TruthValue
    scope_result: TruthValue
    condition_result: TruthValue
    evidence_result: EvaluationResult
    final_result: EvaluationResult
