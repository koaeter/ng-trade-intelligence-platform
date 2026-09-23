from packages.application.source.provision_extraction import ProvisionCandidateExtractor
from packages.domain.source.extraction import ExtractionSegment
from packages.domain.source.provision_candidates import ProvisionCandidateStatus


def test_extraction_segments_become_reviewable_candidates():
    segments = [
        ExtractionSegment(
            id="artifact-1:segment:0",
            artifact_id="artifact-1",
            sequence=0,
            text=" Certificate of origin is required. ",
            page_number=4,
            locator="page=4",
        ),
        ExtractionSegment(
            id="artifact-1:segment:1",
            artifact_id="artifact-1",
            sequence=1,
            text="",
        ),
    ]
    candidates = ProvisionCandidateExtractor().extract("doc-1", segments)

    assert len(candidates) == 1
    assert candidates[0].document_id == "doc-1"
    assert candidates[0].extraction_segment_id == "artifact-1:segment:0"
    assert candidates[0].text == "Certificate of origin is required."
    assert candidates[0].status == ProvisionCandidateStatus.EXTRACTED
    assert candidates[0].candidate_type == "UNCLASSIFIED"


class Documents:
    def get(self, key):
        from packages.domain.source.models import Document
        return Document("doc-1", "source-1", "Doc", "REGULATION")


class Sources:
    def __init__(self):
        from packages.domain.source.models import Source, SourceStatus
        self.value = Source("source-1", "Source", "Authority", "GOV", "NG", "https://example.gov", SourceStatus.EXTRACTED)
        self.updated = None
    def get(self, key):
        return self.value
    def update(self, value):
        self.updated = value


def test_candidate_creation_advances_source_lifecycle():
    sources = Sources()
    segments = [ExtractionSegment("seg-1", "artifact-1", 0, "Requirement text.")]
    candidates = ProvisionCandidateExtractor(Documents(), sources).extract("doc-1", segments)
    assert candidates
    assert sources.updated.status.value == "CANDIDATE"
