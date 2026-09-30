from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ExtractionRun:
    """Immutable record of one bounded extraction execution."""
    id: str
    artifact_id: str
    document_version_id: str | None
    input_checksum_sha256: str
    extractor: str
    extractor_version: str
    extracted_at: datetime
    ocr_used: bool = False


@dataclass(frozen=True)
class ExtractionSegment:
    """A bounded extracted fragment with a stable source location."""
    id: str
    artifact_id: str
    sequence: int
    text: str
    page_number: int | None = None
    section: str | None = None
    source_start: int | None = None
    source_end: int | None = None
    locator: str | None = None
    extraction_id: str | None = None


from enum import StrEnum


class ExtractionComparisonResult(StrEnum):
    SAME_INPUT_SAME_OUTPUT = "SAME_INPUT_SAME_OUTPUT"
    SAME_INPUT_DIFFERENT_OUTPUT = "SAME_INPUT_DIFFERENT_OUTPUT"
    DIFFERENT_INPUT_SAME_OUTPUT = "DIFFERENT_INPUT_SAME_OUTPUT"
    DIFFERENT_INPUT_DIFFERENT_OUTPUT = "DIFFERENT_INPUT_DIFFERENT_OUTPUT"


@dataclass(frozen=True)
class ExtractionComparison:
    """Deterministic comparison of two immutable extraction runs."""
    id: str
    baseline_extraction_id: str
    candidate_extraction_id: str
    baseline_input_checksum_sha256: str
    candidate_input_checksum_sha256: str
    baseline_output_sha256: str
    candidate_output_sha256: str
    result: ExtractionComparisonResult
    compared_at: datetime
