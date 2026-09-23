from dataclasses import dataclass


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
