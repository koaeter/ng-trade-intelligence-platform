from packages.application.source.extraction_repositories import ExtractionSegmentRepository
from packages.domain.source.extraction import ExtractionSegment


class GetExtractionSegment:
    """Read one immutable extraction segment."""

    def __init__(self, segments: ExtractionSegmentRepository) -> None:
        self.segments = segments

    def execute(self, segment_id: str) -> ExtractionSegment:
        for segment in self.segments.list_for_artifact(""):
            if segment.id == segment_id:
                return segment
        raise ValueError("Extraction segment does not exist")


class ListExtractionSegments:
    """List extraction segments for one immutable extraction run."""

    def __init__(self, segments: ExtractionSegmentRepository) -> None:
        self.segments = segments

    def execute(self, extraction_id: str) -> list[ExtractionSegment]:
        return list(self.segments.list_for_extraction(extraction_id))
