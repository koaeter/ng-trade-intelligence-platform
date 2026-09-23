from typing import Protocol

from packages.domain.requirement.candidates import RequirementCandidate


class RequirementCandidateRepository(Protocol):
    def add(self, candidate: RequirementCandidate) -> None: ...

    def get(self, candidate_id: str) -> RequirementCandidate | None: ...

    def list_for_provision(self, provision_id: str) -> list[RequirementCandidate]: ...
