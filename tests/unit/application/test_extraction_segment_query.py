from datetime import datetime, timezone

import pytest

from packages.application.source.extraction_segment_query import (
    GetExtractionSegment,
    ListExtractionSegments,
)
from packages.domain.source.extraction import ExtractionSegment


def segment(segment_id="segment-1", extraction_id="run-1"):
    return ExtractionSegment(segment_id, "artifact-1", 0, "text", extraction_id=extraction_id)


class SegmentRepo:
    def __init__(self, values=None):
        self.values = values or []

    def get(self, segment_id):
        return next((x for x in self.values if x.id == segment_id), None)

    def list_for_artifact(self, artifact_id):
        return [x for x in self.values if x.artifact_id == artifact_id]

    def list_for_extraction(self, extraction_id):
        return [x for x in self.values if x.extraction_id == extraction_id]


def test_get_extraction_segment():
    value = segment()
    assert GetExtractionSegment(SegmentRepo([value])).execute("segment-1") is value


def test_missing_extraction_segment_is_rejected():
    with pytest.raises(ValueError, match="does not exist"):
        GetExtractionSegment(SegmentRepo()).execute("missing")


def test_list_extraction_segments_scopes_to_extraction():
    values = [segment("s1", "run-1"), segment("s2", "run-2"), segment("s3", "run-1")]
    result = ListExtractionSegments(SegmentRepo(values)).execute("run-1")
    assert [x.id for x in result] == ["s1", "s3"]
