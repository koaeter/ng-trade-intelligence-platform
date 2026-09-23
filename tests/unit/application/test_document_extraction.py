from io import BytesIO
from datetime import datetime, timezone
import pytest

from packages.application.source.document_extraction import ExtractionPolicy, ExtractedTextService, TextExtractor
from packages.domain.source.artifacts import ArtifactKind, SourceArtifact

class Store:
    def __init__(self, data): self.data = data
    def get(self, key): return BytesIO(self.data)

def artifact(kind=ArtifactKind.TEXT):
    return SourceArtifact(
        id="artifact-1", source_id="source-1", document_id="doc-1",
        kind=kind, storage_key="source/doc", checksum_sha256="abc",
        acquired_at=datetime.now(timezone.utc),
    )

def test_text_extraction_is_bounded_and_records_metadata():
    result = ExtractedTextService(Store(b"hello"), [TextExtractor()]).extract(artifact())
    assert result.artifact_id == "artifact-1"
    assert result.text == "hello"
    assert result.extractor == "utf8-text-extractor"
    assert result.ocr_used is False

def test_text_extraction_rejects_output_over_limit():
    service = ExtractedTextService(Store(b"12345"), [TextExtractor()], ExtractionPolicy(max_output_characters=4))
    with pytest.raises(ValueError, match="maximum"):
        service.extract(artifact())

def test_unsupported_artifact_kind_is_rejected():
    with pytest.raises(ValueError, match="No extractor"):
        ExtractedTextService(Store(b"x"), [TextExtractor()]).extract(artifact(ArtifactKind.PDF))

def test_invalid_utf8_is_rejected():
    with pytest.raises(ValueError, match="UTF-8"):
        ExtractedTextService(Store(b"\xff"), [TextExtractor()]).extract(artifact(ArtifactKind.TEXT))

def test_domain_conversion_preserves_extraction_metadata():
    result = ExtractedTextService(Store(b"hello"), [TextExtractor()]).extract(artifact())
    domain = ExtractedTextService.to_domain(result)
    assert domain.artifact_id == "artifact-1"
    assert domain.text == "hello"
    assert domain.extractor == "utf8-text-extractor"
