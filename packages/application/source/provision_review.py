from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from packages.domain.source.models import Provision
from packages.domain.source.provision_candidates import ProvisionCandidateStatus
from packages.domain.source.provision_types import ProvisionType


@dataclass(frozen=True)
class ProvisionReviewDecision:
    candidate_id: str
    reviewer_reference: str
    decision: ProvisionCandidateStatus
    provision_type: str | None = None
    reason: str | None = None


class ProvisionReviewService:
    """Governed transition from extracted candidate to authoritative Provision."""

    def __init__(self, candidates, provisions, reviews, documents=None, sources=None) -> None:
        self.candidates = candidates
        self.provisions = provisions
        self.reviews = reviews
        self.documents = documents
        self.sources = sources

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
            self._advance_source_if_review_complete(candidate.document_id)
            return None

        if decision.decision != ProvisionCandidateStatus.ACCEPTED:
            self.candidates.set_status(candidate.id, ProvisionCandidateStatus.REVIEWED)
            return None

        provision_type = (decision.provision_type or "").strip().upper()
        try:
            ProvisionType(provision_type)
        except ValueError as exc:
            raise ValueError("Accepted provision requires a controlled provision type") from exc

        provision = Provision(
            id=str(uuid4()),
            document_id=candidate.document_id,
            locator=candidate.locator,
            text=candidate.text,
            provision_type=provision_type,
        )
        self.provisions.add(provision)
        self.candidates.set_status(candidate.id, ProvisionCandidateStatus.ACCEPTED)
        self._advance_source_if_review_complete(candidate.document_id)
        return provision

    def _advance_source_if_review_complete(self, document_id: str) -> None:
        if self.documents is None or self.sources is None:
            return
        document = self.documents.get(document_id)
        if document is None:
            return
        candidates = self.candidates.list_for_document(document_id)
        terminal = {ProvisionCandidateStatus.ACCEPTED, ProvisionCandidateStatus.REJECTED}
        if not candidates or any(item.status not in terminal for item in candidates):
            return
        source = self.sources.get(document.source_id)
        if source is None:
            return
        from packages.application.source.lifecycle import SourceLifecycleService
        from packages.domain.source.models import SourceStatus
        if source.status == SourceStatus.CANDIDATE:
            self.sources.update(
                SourceLifecycleService().transition(source, SourceStatus.REVIEWED)
            )
