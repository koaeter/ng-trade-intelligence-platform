from typing import Protocol
from packages.domain.source.extraction import ExtractionSegment


class ExtractionSegmentRepository(Protocol):
    def add(self, segment: ExtractionSegment) -> None: ...
    def list_for_artifact(self, artifact_id: str) -> list[ExtractionSegment]: ...
