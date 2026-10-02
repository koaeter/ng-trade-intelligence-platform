from dataclasses import dataclass
from enum import StrEnum
from datetime import datetime


class ExtractionDiffEntryType(StrEnum):
    UNCHANGED = "UNCHANGED"
    ADDED = "ADDED"
    REMOVED = "REMOVED"
    MODIFIED = "MODIFIED"


@dataclass(frozen=True)
class ExtractionDiff:
    """Immutable, auditable segment-level diff between two extraction runs."""
    id: str
    comparison_id: str
    baseline_extraction_id: str
    candidate_extraction_id: str
    entry_count: int
    unchanged_count: int
    added_count: int
    removed_count: int
    modified_count: int
    created_at: datetime


@dataclass(frozen=True)
class ExtractionDiffEntry:
    """One deterministic segment-level change with both source locations."""
    id: str
    diff_id: str
    entry_type: ExtractionDiffEntryType
    ordinal: int
    baseline_segment_id: str | None
    candidate_segment_id: str | None
    baseline_sequence: int | None
    candidate_sequence: int | None
    baseline_text_sha256: str | None
    candidate_text_sha256: str | None
    baseline_page_number: int | None
    candidate_page_number: int | None
    baseline_section: str | None
    candidate_section: str | None
    baseline_source_start: int | None
    baseline_source_end: int | None
    candidate_source_start: int | None
    candidate_source_end: int | None
    baseline_locator: str | None
    candidate_locator: str | None
