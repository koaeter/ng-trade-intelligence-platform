from dataclasses import dataclass
from datetime import date
from enum import Enum


class EvaluationResult(str, Enum):
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNRESOLVED = "UNRESOLVED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    CONFLICTING = "CONFLICTING"


@dataclass(frozen=True)
class ExportScenario:
    id: str
    product_id: str
    hs_code: str
    origin_country_code: str
    destination_market_code: str
    scenario_date: date


@dataclass(frozen=True)
class ApplicabilityEvaluation:
    scenario_id: str
    result: EvaluationResult
    rule_set_version: str
