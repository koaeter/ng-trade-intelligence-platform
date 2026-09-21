from dataclasses import dataclass
from datetime import date
from enum import Enum

from packages.domain.evidence.models import Evidence
from packages.domain.catalog.models import Country, HSCode, Market, Product


class EvaluationResult(str, Enum):
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNRESOLVED = "UNRESOLVED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    CONFLICTING = "CONFLICTING"


@dataclass(frozen=True)
class ExportScenario:
    id: str
    product: Product
    hs_code: HSCode
    origin_country: Country
    destination_market: Market
    scenario_date: date


@dataclass(frozen=True)
class ApplicabilityEvaluation:
    scenario_id: str
    requirement_id: str
    result: EvaluationResult
    rule_set_version: str
    evidence: tuple[Evidence, ...] = ()
