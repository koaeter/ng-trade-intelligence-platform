from packages.application.source.provision_review import (
    ProvisionReviewDecision, ProvisionReviewService,
)
from packages.domain.source.provision_candidates import (
    ProvisionCandidate, ProvisionCandidateStatus,
)


class Candidates:
    def __init__(self, candidate):
        self.candidate = candidate
        self.status = candidate.status

    def get(self, candidate_id):
        return self.candidate if candidate_id == self.candidate.id else None

    def set_status(self, candidate_id, status):
        assert candidate_id == self.candidate.id
        self.status = status


class Provisions:
    def __init__(self):
        self.items = []

    def add(self, provision):
        self.items.append(provision)


class Reviews:
    def __init__(self):
        self.items = []

    def add(self, *args):
        self.items.append(args)


def candidate():
    return ProvisionCandidate(
        id="candidate-1",
        document_id="doc-1",
        artifact_id="artifact-1",
        extraction_segment_id="artifact-1:segment:0",
        text="Certificate of origin is required.",
        locator="page=4",
    )


def test_accepted_candidate_becomes_provision():
    candidates = Candidates(candidate())
    provisions = Provisions()
    service = ProvisionReviewService(candidates, provisions, Reviews())

    provision = service.review(
        ProvisionReviewDecision(
            "candidate-1", "reviewer-1", ProvisionCandidateStatus.ACCEPTED,
            "DOCUMENT_REQUIREMENT",
        )
    )

    assert provision is not None
    assert provision.document_id == "doc-1"
    assert provision.locator == "page=4"
    assert candidates.status == ProvisionCandidateStatus.ACCEPTED


def test_rejected_candidate_does_not_become_provision():
    candidates = Candidates(candidate())
    provisions = Provisions()
    service = ProvisionReviewService(candidates, provisions, Reviews())

    provision = service.review(
        ProvisionReviewDecision(
            "candidate-1", "reviewer-1", ProvisionCandidateStatus.REJECTED,
            reason="Not a regulatory provision.",
        )
    )

    assert provision is None
    assert provisions.items == []
    assert candidates.status == ProvisionCandidateStatus.REJECTED


def test_accepted_candidate_rejects_unknown_provision_type():
    candidates = Candidates(candidate())
    service = ProvisionReviewService(candidates, Provisions(), Reviews())

    try:
        service.review(
            ProvisionReviewDecision(
                "candidate-1", "reviewer-1", ProvisionCandidateStatus.ACCEPTED,
                "MADE_UP_TYPE",
            )
        )
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "controlled provision type" in str(exc)
