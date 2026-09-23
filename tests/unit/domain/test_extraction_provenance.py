from packages.domain.source.extraction import ExtractionSegment


def test_extraction_segment_preserves_document_location() -> None:
    segment = ExtractionSegment(id="seg-1", artifact_id="artifact-1", sequence=3,
        text="Certificate of origin is required.", page_number=12, section="Schedule 2",
        source_start=420, source_end=455, locator="page=12;section=Schedule 2")
    assert segment.artifact_id == "artifact-1"
    assert segment.sequence == 3
    assert segment.page_number == 12
    assert segment.section == "Schedule 2"
    assert segment.source_start == 420
    assert segment.source_end == 455
