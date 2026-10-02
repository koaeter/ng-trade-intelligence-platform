from packages.application.source.extraction_repositories import ExtractionSegmentRepository
from packages.domain.source.extraction import ExtractionSegment


class GetExtractionSegment:
    """Read one immutable extraction segment."""

    def __init__(self, segments: ExtractionSegmentRepository) -> None:
        self.segments = segments

    def execute(self, segment_id: str) -> ExtractionSegment:
        segment = self.segments.get(segment_id)
        if segment is None:
            raise ValueError("Extraction segment does not exist")
        return segment


class ListExtractionSegments:
    """List extraction segments for one immutable extraction run."""

    def __init__(self, segments: ExtractionSegmentRepository) -> None:
        self.segments = segments

    def execute(self, extraction_id: str) -> list[ExtractionSegment]:
        return list(self.segments.list_for_extraction(extraction_id))
