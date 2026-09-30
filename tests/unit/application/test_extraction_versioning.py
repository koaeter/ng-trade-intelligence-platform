from datetime import datetime, timezone

from packages.application.source.document_extraction import ExtractedTextService, TextExtractor
from packages.domain.source.artifacts import ArtifactKind, SourceArtifact
from packages.domain.source.extraction import ExtractionRun


class Store:
    def get(self, key):
        from io import BytesIO
        return BytesIO(b"first\nsecond")


def artifact():
    return SourceArtifact(
        id="artifact-1",
        source_id="source-1",
        document_id="doc-1",
        document_version_id="version-1",
        kind=ArtifactKind.TEXT,
        storage_key="source/doc",
        checksum_sha256="a" * 64,
        acquired_at=datetime.now(timezone.utc),
    )


def test_extraction_result_has_unique_run_identity():
    service = ExtractedTextService(Store(), [TextExtractor()])
    first = service.extract(artifact())
    second = service.extract(artifact())
    assert first.extraction_id
    assert second.extraction_id
    assert first.extraction_id != second.extraction_id


def test_extraction_run_carries_artifact_version_and_checksum():
    service = ExtractedTextService(Store(), [TextExtractor()])
    result = service.extract(artifact())
    run = service.to_extraction_run(result, artifact())
    assert isinstance(run, ExtractionRun)
    assert run.artifact_id == "artifact-1"
    assert run.document_version_id == "version-1"
    assert run.input_checksum_sha256 == "a" * 64
    assert run.extractor_version == "2"


def test_segments_bind_to_extraction_run():
    service = ExtractedTextService(Store(), [TextExtractor()])
    result = service.extract(artifact())
    segments = service.to_segments(result)
    assert all(segment.extraction_id == result.extraction_id for segment in segments)
    assert segments[0].id.startswith(result.extraction_id + ":segment:")
