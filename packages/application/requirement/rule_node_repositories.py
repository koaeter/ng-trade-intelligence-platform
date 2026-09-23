from typing import Protocol

from packages.domain.requirement.rule_nodes import RequirementRuleNode


class RequirementRuleNodeRepository(Protocol):
    def add(self, node: RequirementRuleNode) -> None: ...

    def list_for_requirement(self, requirement_id: str) -> list[RequirementRuleNode]: ...

    def list_for_revision(self, requirement_revision_id: str) -> list[RequirementRuleNode]: ...
