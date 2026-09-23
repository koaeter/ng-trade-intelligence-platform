from packages.application.source.source_ingestion import SourceIngestionService
from packages.application.source.source_acquisition import AcquiredSourceResponse


class Acquisition:
    def acquire(self, key, content, content_type):
        class Result:
            storage_key = key
            checksum_sha256 = "a" * 64
        return Result()


class Sources:
    def __init__(self):
        from packages.domain.source.models import Source, SourceStatus
        self.value = Source("source-1", "Source", "Authority", "GOV", "NG", "https://example.gov", SourceStatus.DISCOVERED)
        self.updated = None
    def get(self, key):
        return self.value
    def update(self, value):
        self.updated = value


class Artifacts:
    def __init__(self):
        self.items = []
    def add(self, artifact):
        self.items.append(artifact)


def test_source_ingestion_creates_acquired_artifact():
    artifacts = Artifacts()
    response = AcquiredSourceResponse(
        "https://example.gov/rules.pdf",
        "application/pdf",
        b"%PDF-test",
    )
    sources = Sources()
    artifact = SourceIngestionService(Acquisition(), artifacts, sources).ingest(
        "source-1", "document-1", "source-1/document-1.pdf", response
    )
    assert artifact.source_id == "source-1"
    assert artifact.document_id == "document-1"
    assert artifact.kind.value == "PDF"
    assert artifacts.items == [artifact]
    assert sources.updated.status.value == "ACQUIRED"
