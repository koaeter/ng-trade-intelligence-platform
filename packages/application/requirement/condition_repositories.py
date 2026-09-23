from typing import Protocol

from packages.domain.requirement.conditions import RequirementConditionCandidate


class RequirementConditionCandidateRepository(Protocol):
    def add(self, condition: RequirementConditionCandidate) -> None: ...

    def list_for_candidate(self, candidate_id: str) -> list[RequirementConditionCandidate]: ...
