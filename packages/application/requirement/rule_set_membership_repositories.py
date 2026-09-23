from typing import Protocol

from packages.domain.requirement.rule_set_membership import RuleSetRequirementMembership


class RuleSetMembershipRepository(Protocol):
    def add(self, membership: RuleSetRequirementMembership) -> None: ...

    def list_for_rule_set(self, rule_set_id: str) -> list[RuleSetRequirementMembership]: ...
