from datetime import datetime
from typing import Protocol


class RequirementCandidateReviewRepository(Protocol):
    def add(
        self,
        candidate_id: str,
        reviewer_reference: str,
        scope_reviewed: bool,
        reviewed_at: datetime,
    ) -> None: ...
