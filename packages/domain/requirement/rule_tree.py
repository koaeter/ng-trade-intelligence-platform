from dataclasses import dataclass
from enum import Enum

from packages.domain.requirement.conditions import RequirementConditionCandidate


class ConditionGroupOperator(str, Enum):
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


@dataclass(frozen=True)
class ConditionLeaf:
    condition: RequirementConditionCandidate


@dataclass(frozen=True)
class ConditionGroup:
    operator: ConditionGroupOperator
    children: tuple["ConditionNode", ...]


ConditionNode = ConditionLeaf | ConditionGroup
