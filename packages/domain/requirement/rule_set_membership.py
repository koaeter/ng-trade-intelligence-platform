from dataclasses import dataclass


@dataclass(frozen=True)
class RuleSetRequirementMembership:
    rule_set_id: str
    requirement_id: str
    requirement_revision: str
