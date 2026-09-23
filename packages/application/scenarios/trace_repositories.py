from typing import Protocol

from packages.domain.scenario.applicability_trace import ApplicabilityTrace


class ApplicabilityTraceRepository(Protocol):
    def add(self, trace: ApplicabilityTrace, rule_set_version: str) -> None: ...

    def list_for_scenario(self, scenario_id: str) -> list[ApplicabilityTrace]: ...
