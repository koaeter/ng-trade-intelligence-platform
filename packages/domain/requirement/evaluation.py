from dataclasses import dataclass
from enum import Enum

from packages.domain.requirement.conditions import (
    RequirementConditionCandidate, RequirementConditionOperator,
)


class TruthValue(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ConditionEvaluation:
    condition: RequirementConditionCandidate
    result: TruthValue
    reason: str


@dataclass(frozen=True)
class ConditionSetEvaluation:
    result: TruthValue
    conditions: tuple[ConditionEvaluation, ...]
