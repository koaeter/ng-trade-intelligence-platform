from typing import Protocol

from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion


class RuleSetVersionRepository(Protocol):
    def get(self, version_id: str) -> RuleSetVersion | None: ...

    def get_active(self) -> RuleSetVersion | None: ...

    def set_status(self, version_id: str, status: RuleSetStatus) -> None: ...
