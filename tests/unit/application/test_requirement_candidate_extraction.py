from packages.application.requirement.candidate_extraction import RequirementCandidateExtractor
from packages.domain.requirement.candidates import RequirementCandidateStatus
from packages.domain.source.models import Provision


def test_provision_becomes_reviewable_requirement_candidate():
    provision = Provision(
        "provision-1",
        "doc-1",
        "page=4",
        "An exporter must obtain a certificate of origin before export.",
        "DOCUMENT_REQUIREMENT",
    )
    candidates = RequirementCandidateExtractor().extract([provision])

    assert len(candidates) == 1
    assert candidates[0].provision_id == "provision-1"
    assert candidates[0].document_id == "doc-1"
    assert candidates[0].status == RequirementCandidateStatus.EXTRACTED
    assert candidates[0].proposed_name.startswith("An exporter must obtain")
