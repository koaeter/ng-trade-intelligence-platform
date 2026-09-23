from packages.application.source.provision_evidence import ProvisionEvidenceService
from packages.domain.source.models import Document, Provision
from packages.domain.source.provision_candidates import ProvisionCandidate


class Documents:
    def get(self, document_id):
        return Document(document_id, "source-1", "Export Regulation", "REGULATION")


class EvidenceRepo:
    def __init__(self):
        self.items = []

    def add(self, evidence):
        self.items.append(evidence)


def test_accepted_provision_gets_verified_source_evidence():
    evidence = EvidenceRepo()
    service = ProvisionEvidenceService(Documents(), evidence)
    candidate = ProvisionCandidate(
        "candidate-1", "doc-1", "artifact-1", "artifact-1:segment:2",
        "Certificate required.", "page=4",
    )
    provision = Provision("provision-1", "doc-1", "page=4", "Certificate required.", "CERTIFICATE")

    result = service.attach_verified_source_evidence(provision, candidate)

    assert result.source_id == "source-1"
    assert result.document_id == "doc-1"
    assert result.provision_id == "provision-1"
    assert result.verified is True
    assert "artifact-1:segment:2" in result.locator
    assert evidence.items == [result]
