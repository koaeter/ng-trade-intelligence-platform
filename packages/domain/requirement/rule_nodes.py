from dataclasses import dataclass
from enum import Enum

from packages.domain.requirement.conditions import (
    RequirementConditionField, RequirementConditionOperator,
)
from packages.domain.requirement.rule_tree import ConditionGroupOperator


class RequirementRuleNodeType(str, Enum):
    GROUP = "GROUP"
    CONDITION = "CONDITION"


@dataclass(frozen=True)
class RequirementRuleNode:
    id: str
    requirement_id: str
    requirement_revision_id: str
    parent_id: str | None
    sequence: int
    node_type: RequirementRuleNodeType
    group_operator: ConditionGroupOperator | None = None
    field: RequirementConditionField | None = None
    operator: RequirementConditionOperator | None = None
    value: str | None = None
