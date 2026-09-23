from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ArtifactKind(str, Enum):
    PDF = "PDF"
    HTML = "HTML"
    DOCX = "DOCX"
    XLSX = "XLSX"
    CSV = "CSV"
    IMAGE = "IMAGE"
    TEXT = "TEXT"
    OTHER = "OTHER"


class ArtifactProcessingState(str, Enum):
    ACQUIRED = "ACQUIRED"
    EXTRACTED = "EXTRACTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class SourceArtifact:
    id: str
    source_id: str
    document_id: str
    kind: ArtifactKind
    storage_key: str
    checksum_sha256: str
    acquired_at: datetime
    mime_type: str | None = None
    original_filename: str | None = None
    processing_state: ArtifactProcessingState = ArtifactProcessingState.ACQUIRED
    acquisition_event_id: str | None = None


@dataclass(frozen=True)
class ExtractedText:
    artifact_id: str
    text: str
    extractor: str
    extractor_version: str
    extracted_at: datetime
    ocr_used: bool = False
