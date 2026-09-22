from datetime import datetime, timezone

import pytest

from packages.application.ingestion.artifact_service import DocumentArtifactService
from packages.domain.source.artifacts import ArtifactKind, ArtifactProcessingState, ExtractedText, SourceArtifact


class Store:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)


def test_register_acquired_artifact_and_record_extraction():
    artifacts = Store()
    texts = Store()
    service = DocumentArtifactService(artifacts, texts)
    artifact = SourceArtifact(
        "artifact-1", "source-1", "document-1", ArtifactKind.PDF,
        "objects/document-1.pdf", "abc123", datetime.now(timezone.utc)
    )
    extracted = ExtractedText("artifact-1", "section text", "test-extractor", "1.0", datetime.now(timezone.utc))

    service.register_acquired_artifact(artifact)
    service.record_extraction(artifact, extracted)

    assert artifacts.items == [artifact]
    assert texts.items == [extracted]


def test_artifact_must_start_acquired():
    service = DocumentArtifactService(Store(), Store())
    artifact = SourceArtifact(
        "artifact-1", "source-1", "document-1", ArtifactKind.PDF,
        "objects/document-1.pdf", "abc123", datetime.now(timezone.utc),
        processing_state=ArtifactProcessingState.EXTRACTED
    )

    with pytest.raises(ValueError, match="ACQUIRED"):
        service.register_acquired_artifact(artifact)


def test_extracted_text_must_reference_artifact():
    service = DocumentArtifactService(Store(), Store())
    artifact = SourceArtifact(
        "artifact-1", "source-1", "document-1", ArtifactKind.PDF,
        "objects/document-1.pdf", "abc123", datetime.now(timezone.utc)
    )
    extracted = ExtractedText("different-artifact", "text", "extractor", "1.0", datetime.now(timezone.utc))

    with pytest.raises(ValueError, match="artifact"):
        service.record_extraction(artifact, extracted)
