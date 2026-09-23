from uuid import uuid4

from packages.domain.evidence.models import Evidence
from packages.domain.source.models import Provision
from packages.domain.source.provision_candidates import ProvisionCandidate


class ProvisionEvidenceService:
    """Attaches the accepted candidate's exact extraction location to a Provision."""

    def __init__(self, documents, evidence) -> None:
        self.documents = documents
        self.evidence = evidence

    def attach_verified_source_evidence(
        self,
        provision: Provision,
        candidate: ProvisionCandidate,
    ) -> Evidence:
        if provision.document_id != candidate.document_id:
            raise ValueError("Provision and candidate must belong to the same document")
        document = self.documents.get(candidate.document_id)
        if document is None:
            raise ValueError("Provision document does not exist")

        locator = f"segment={candidate.extraction_segment_id};{candidate.locator}"
        evidence = Evidence(
            id=str(uuid4()),
            evidence_type="REGULATORY_PROVISION",
            source_id=document.source_id,
            locator=locator,
            excerpt=candidate.text,
            verified=True,
            document_id=candidate.document_id,
            provision_id=provision.id,
        )
        self.evidence.add(evidence)
        return evidence
