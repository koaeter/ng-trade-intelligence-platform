from datetime import datetime, timezone

from infrastructure.database.models import SourceArtifactModel
from infrastructure.database.repositories import (
    SqlAlchemyExtractedTextRepository,
    SqlAlchemySourceArtifactRepository,
)
from packages.domain.source.artifacts import ArtifactKind, ExtractedText, SourceArtifact


class FakeSession:
    def __init__(self):
        self.items = {}

    def add(self, item):
        key = getattr(item, "id", getattr(item, "artifact_id", None))
        self.items[(type(item), key)] = item

    def flush(self):
        return None

    def get(self, model, key):
        return self.items.get((model, key))


def test_artifact_repository_round_trip():
    session = FakeSession()
    repo = SqlAlchemySourceArtifactRepository(session)
    artifact = SourceArtifact(
        "artifact-1", "source-1", "document-1", ArtifactKind.PDF,
        "objects/source-1/document-1.pdf", "a" * 64,
        datetime.now(timezone.utc), "application/pdf", "document.pdf",
    )
    repo.add(artifact)
    assert repo.get("artifact-1") == artifact


def test_extracted_text_repository_round_trip():
    session = FakeSession()
    repo = SqlAlchemyExtractedTextRepository(session)
    extracted = ExtractedText(
        "artifact-1", "regulatory text", "pdf-extractor", "2.1",
        datetime.now(timezone.utc), True,
    )
    repo.add(extracted)
    assert repo.get("artifact-1") == extracted


def test_artifact_model_has_provider_neutral_storage_key():
    assert "storage_key" in SourceArtifactModel.__table__.columns
