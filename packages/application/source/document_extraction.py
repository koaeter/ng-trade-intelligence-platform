from dataclasses import dataclass
from typing import BinaryIO, Protocol

from packages.application.source.object_storage import ObjectStorage
from packages.domain.source.artifacts import ArtifactKind, ExtractedText, SourceArtifact


@dataclass(frozen=True)
class ExtractionPolicy:
    max_output_characters: int = 2_000_000
    max_pages: int = 500


@dataclass(frozen=True)
class ExtractionResult:
    artifact_id: str
    text: str
    extractor: str
    extractor_version: str
    ocr_used: bool
    page_count: int | None = None


class DocumentExtractor(Protocol):
    supported_kinds: frozenset[ArtifactKind]

    def extract(self, content: BinaryIO, policy: ExtractionPolicy) -> ExtractionResult: ...


class TextExtractor:
    supported_kinds = frozenset({ArtifactKind.TEXT, ArtifactKind.HTML, ArtifactKind.CSV})

    def extract(self, content: BinaryIO, policy: ExtractionPolicy) -> ExtractionResult:
        data = content.read(policy.max_output_characters + 1)
        if len(data) > policy.max_output_characters:
            raise ValueError("Extracted text exceeds configured maximum")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Text artifact is not valid UTF-8") from exc
        return ExtractionResult("", text, "utf8-text-extractor", "1", False)


class ExtractedTextService:
    """Coordinates bounded extraction; parser implementations remain infrastructure concerns."""

    def __init__(self, storage: ObjectStorage, extractors: list[DocumentExtractor],
                 policy: ExtractionPolicy | None = None) -> None:
        self.storage = storage
        self.extractors = extractors
        self.policy = policy or ExtractionPolicy()

    def extract(self, artifact: SourceArtifact) -> ExtractionResult:
        extractor = next((x for x in self.extractors if artifact.kind in x.supported_kinds), None)
        if extractor is None:
            raise ValueError(f"No extractor registered for artifact kind: {artifact.kind.value}")
        with self.storage.get(artifact.storage_key) as content:
            result = extractor.extract(content, self.policy)
        return ExtractionResult(
            artifact.id, result.text, result.extractor, result.extractor_version,
            result.ocr_used, result.page_count,
        )

    @staticmethod
    def to_domain(result: ExtractionResult) -> ExtractedText:
        from datetime import datetime, timezone
        return ExtractedText(
            artifact_id=result.artifact_id,
            text=result.text,
            extractor=result.extractor,
            extractor_version=result.extractor_version,
            extracted_at=datetime.now(timezone.utc),
            ocr_used=result.ocr_used,
        )
