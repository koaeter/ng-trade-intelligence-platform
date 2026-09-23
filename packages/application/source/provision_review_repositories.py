from datetime import datetime
from typing import Protocol

from packages.domain.source.provision_candidates import ProvisionCandidateStatus


class ProvisionCandidateReviewRepository(Protocol):
    def add(
        self,
        candidate_id: str,
        reviewer_reference: str,
        decision: ProvisionCandidateStatus,
        reason: str | None,
        reviewed_at: datetime,
    ) -> None: ...
