from typing import Protocol

from packages.domain.requirement.rule_set_membership import RuleSetRequirementMembership
from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion


class RuleSetVersionRepository(Protocol):
    def add(self, version: RuleSetVersion) -> None: ...

    def get(self, version_id: str) -> RuleSetVersion | None: ...

    def get_active(self) -> RuleSetVersion | None: ...

    def set_status(self, version_id: str, status: RuleSetStatus) -> None: ...


class RuleSetMembershipRepository(Protocol):
    def add(self, membership: RuleSetRequirementMembership) -> None: ...

    def list_for_rule_set(self, rule_set_id: str) -> list[RuleSetRequirementMembership]: ...
