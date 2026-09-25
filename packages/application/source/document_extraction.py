from dataclasses import dataclass
from typing import BinaryIO, Protocol

from packages.application.source.object_storage import ObjectStorage
from packages.domain.source.artifacts import ArtifactKind, ExtractedText, SourceArtifact
from packages.domain.source.extraction import ExtractionSegment


@dataclass(frozen=True)
class ExtractionPolicy:
    max_input_bytes: int = 50_000_000
    max_output_characters: int = 2_000_000
    max_pages: int = 500
    max_zip_members: int = 5_000
    max_zip_member_bytes: int = 20_000_000
    max_zip_uncompressed_bytes: int = 100_000_000


@dataclass(frozen=True)
class ExtractionFragment:
    text: str
    page_number: int | None = None
    section: str | None = None
    locator: str | None = None


@dataclass(frozen=True)
class ExtractionResult:
    artifact_id: str
    text: str
    extractor: str
    extractor_version: str
    ocr_used: bool
    page_count: int | None = None
    fragments: tuple[ExtractionFragment, ...] = ()


class DocumentExtractor(Protocol):
    supported_kinds: frozenset[ArtifactKind]

    def extract(
        self,
        artifact: SourceArtifact,
        content: BinaryIO,
        policy: ExtractionPolicy,
    ) -> ExtractionResult: ...


class TextExtractor:
    supported_kinds = frozenset({ArtifactKind.TEXT, ArtifactKind.HTML, ArtifactKind.CSV})

    def extract(
        self,
        artifact: SourceArtifact,
        content: BinaryIO,
        policy: ExtractionPolicy,
    ) -> ExtractionResult:
        data = _read_bounded(content, policy.max_input_bytes)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Text artifact is not valid UTF-8") from exc
        if len(text) > policy.max_output_characters:
            raise ValueError("Extracted text exceeds configured maximum")
        lines = tuple(line.strip() for line in text.splitlines() if line.strip())
        fragments = tuple(
            ExtractionFragment(line, locator=f"line={index}")
            for index, line in enumerate(lines, 1)
        )
        return ExtractionResult(
            artifact.id, text, "utf8-text-extractor", "2", False, None, fragments
        )


class ExtractedTextService:
    """Coordinates bounded extraction; parser implementations remain infrastructure concerns."""

    def __init__(self, storage: ObjectStorage, extractors: list[DocumentExtractor],
                 policy: ExtractionPolicy | None = None, sources=None) -> None:
        self.storage = storage
        self.extractors = extractors
        self.policy = policy or ExtractionPolicy()
        self.sources = sources

    def extract(self, artifact: SourceArtifact) -> ExtractionResult:
        extractor = next((x for x in self.extractors if artifact.kind in x.supported_kinds), None)
        if extractor is None:
            raise ValueError(f"No extractor registered for artifact kind: {artifact.kind.value}")
        with self.storage.get(artifact.storage_key) as content:
            result = extractor.extract(artifact, content, self.policy)
        if result.artifact_id != artifact.id:
            raise ValueError("Extractor returned an unexpected artifact ID")
        final = ExtractionResult(
            artifact.id, result.text, result.extractor, result.extractor_version,
            result.ocr_used, result.page_count, result.fragments,
        )
        if self.sources is not None:
            source = self.sources.get(artifact.source_id)
            if source is not None:
                from packages.application.source.lifecycle import SourceLifecycleService
                from packages.domain.source.models import SourceStatus
                if source.status == SourceStatus.ACQUIRED:
                    self.sources.update(
                        SourceLifecycleService().transition(source, SourceStatus.EXTRACTED)
                    )
        return final

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

    @staticmethod
    def to_segments(result: ExtractionResult) -> tuple[ExtractionSegment, ...]:
        return tuple(
            ExtractionSegment(
                id=f"{result.artifact_id}:segment:{index}",
                artifact_id=result.artifact_id,
                sequence=index,
                text=fragment.text,
                page_number=fragment.page_number,
                section=fragment.section,
                source_start=None,
                source_end=None,
                locator=fragment.locator,
            )
            for index, fragment in enumerate(result.fragments)
        )


def _read_bounded(content: BinaryIO, maximum: int) -> bytes:
    if maximum <= 0:
        raise ValueError("Extraction input limit must be positive")
    data = content.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError("Source artifact exceeds configured input limit")
    return data
