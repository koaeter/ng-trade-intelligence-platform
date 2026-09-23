from typing import Protocol

from packages.domain.source.provision_candidates import ProvisionCandidate


class ProvisionCandidateRepository(Protocol):
    def add(self, candidate: ProvisionCandidate) -> None: ...

    def get(self, candidate_id: str) -> ProvisionCandidate | None: ...

    def list_for_document(self, document_id: str) -> list[ProvisionCandidate]: ...
