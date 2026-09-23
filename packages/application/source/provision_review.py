from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from packages.domain.source.models import Provision
from packages.domain.source.provision_candidates import ProvisionCandidate, ProvisionCandidateStatus


@dataclass(frozen=True)
class ProvisionReviewDecision:
    candidate_id: str
    reviewer_reference: str
    decision: ProvisionCandidateStatus
    provision_type: str | None = None
    reason: str | None = None


class ProvisionReviewService:
    """Governed transition from extracted candidate to authoritative Provision."""

    def __init__(self, candidates, provisions, reviews) -> None:
        self.candidates = candidates
        self.provisions = provisions
        self.reviews = reviews

    def review(self, decision: ProvisionReviewDecision) -> Provision | None:
        candidate = self.candidates.get(decision.candidate_id)
        if candidate is None:
            raise ValueError("Provision candidate does not exist")
        if candidate.status not in {
            ProvisionCandidateStatus.EXTRACTED,
            ProvisionCandidateStatus.REVIEWED,
        }:
            raise ValueError("Provision candidate is not reviewable")
        if not decision.reviewer_reference.strip():
            raise ValueError("Reviewer reference is required")

        self.reviews.add(
            decision.candidate_id,
            decision.reviewer_reference,
            decision.decision,
            decision.reason,
            datetime.now(timezone.utc),
        )

        if decision.decision == ProvisionCandidateStatus.REJECTED:
            self.candidates.set_status(candidate.id, ProvisionCandidateStatus.REJECTED)
            return None

        if decision.decision != ProvisionCandidateStatus.ACCEPTED:
            self.candidates.set_status(candidate.id, ProvisionCandidateStatus.REVIEWED)
            return None

        provision_type = (decision.provision_type or "").strip()
        if not provision_type:
            raise ValueError("Accepted provision requires a provision type")

        provision = Provision(
            id=str(uuid4()),
            document_id=candidate.document_id,
            locator=candidate.locator,
            text=candidate.text,
            provision_type=provision_type,
        )
        self.provisions.add(provision)
        self.candidates.set_status(candidate.id, ProvisionCandidateStatus.ACCEPTED)
        return provision
