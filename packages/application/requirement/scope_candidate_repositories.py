from typing import Protocol

from packages.domain.requirement.scope_candidates import RequirementScopeCandidate


class RequirementScopeCandidateRepository(Protocol):
    def add(self, scope: RequirementScopeCandidate) -> None: ...

    def get(self, candidate_id: str) -> RequirementScopeCandidate | None: ...
