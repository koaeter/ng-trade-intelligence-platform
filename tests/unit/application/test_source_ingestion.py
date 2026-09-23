from packages.application.source.source_ingestion import SourceIngestionService
from packages.application.source.source_acquisition import AcquiredSourceResponse


class Acquisition:
    def acquire(self, key, content, content_type):
        class Result:
            storage_key = key
            checksum_sha256 = "a" * 64
        return Result()


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
    artifact = SourceIngestionService(Acquisition(), artifacts).ingest(
        "source-1", "document-1", "source-1/document-1.pdf", response
    )
    assert artifact.source_id == "source-1"
    assert artifact.document_id == "document-1"
    assert artifact.kind.value == "PDF"
    assert artifacts.items == [artifact]
