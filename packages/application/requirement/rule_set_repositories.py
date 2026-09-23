from typing import Protocol

from packages.domain.requirement.rule_sets import RuleSetVersion


class RuleSetVersionRepository(Protocol):
    def get_active(self) -> RuleSetVersion | None: ...
