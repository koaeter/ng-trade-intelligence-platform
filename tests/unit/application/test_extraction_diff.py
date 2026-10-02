from datetime import datetime, timezone

import pytest

from packages.application.source.extraction_diff import CompareExtractionSegments
from packages.domain.source.extraction import ExtractionComparison, ExtractionSegment
from packages.domain.source.extraction_diff import ExtractionDiffEntryType


def comparison():
    return ExtractionComparison(
        "cmp-1", "run-a", "run-b", "a" * 64, "b" * 64,
        "c" * 64, "d" * 64, "DIFFERENT_INPUT_DIFFERENT_OUTPUT",
        datetime.now(timezone.utc),
    )


def seg(run_id, segment_id, text, sequence, **kwargs):
    return ExtractionSegment(segment_id, "artifact-1", sequence, text, extraction_id=run_id, **kwargs)


def types(entries):
    return [entry.entry_type for entry in entries]


def test_unchanged_segments_are_matched():
    diff, entries = CompareExtractionSegments().execute(
        comparison(),
        [seg("run-a", "a1", "one", 1), seg("run-a", "a2", "two", 2)],
        [seg("run-b", "b1", "one", 1), seg("run-b", "b2", "two", 2)],
    )
    assert types(entries) == [ExtractionDiffEntryType.UNCHANGED, ExtractionDiffEntryType.UNCHANGED]
    assert diff.unchanged_count == 2
    assert diff.entry_count == 2


def test_insertion_does_not_shift_following_segments_into_modifications():
    diff, entries = CompareExtractionSegments().execute(
        comparison(),
        [seg("run-a", "a1", "one", 1), seg("run-a", "a2", "two", 2)],
        [seg("run-b", "b1", "one", 1), seg("run-b", "b2", "inserted", 2), seg("run-b", "b3", "two", 3)],
    )
    assert types(entries) == [ExtractionDiffEntryType.UNCHANGED, ExtractionDiffEntryType.ADDED, ExtractionDiffEntryType.UNCHANGED]
    assert diff.added_count == 1


def test_replacement_is_modified_and_preserves_locations():
    diff, entries = CompareExtractionSegments().execute(
        comparison(),
        [seg("run-a", "a1", "old text", 4, page_number=2, locator="p2:s4")],
        [seg("run-b", "b1", "new text", 4, page_number=3, locator="p3:s4")],
    )
    entry = entries[0]
    assert entry.entry_type == ExtractionDiffEntryType.MODIFIED
    assert entry.baseline_segment_id == "a1"
    assert entry.candidate_segment_id == "b1"
    assert entry.baseline_page_number == 2
    assert entry.candidate_page_number == 3
    assert entry.baseline_locator == "p2:s4"
    assert entry.candidate_locator == "p3:s4"
    assert diff.modified_count == 1


def test_unbalanced_replacement_creates_modified_plus_additions():
    diff, entries = CompareExtractionSegments().execute(
        comparison(),
        [seg("run-a", "a1", "old", 1)],
        [seg("run-b", "b1", "new", 1), seg("run-b", "b2", "extra", 2)],
    )
    assert types(entries) == [ExtractionDiffEntryType.MODIFIED, ExtractionDiffEntryType.ADDED]
    assert diff.modified_count == 1
    assert diff.added_count == 1


def test_removal_is_preserved():
    diff, entries = CompareExtractionSegments().execute(
        comparison(),
        [seg("run-a", "a1", "one", 1), seg("run-a", "a2", "removed", 2), seg("run-a", "a3", "three", 3)],
        [seg("run-b", "b1", "one", 1), seg("run-b", "b3", "three", 2)],
    )
    assert types(entries) == [ExtractionDiffEntryType.UNCHANGED, ExtractionDiffEntryType.REMOVED, ExtractionDiffEntryType.UNCHANGED]
    assert diff.removed_count == 1


def test_segments_must_belong_to_the_compared_run():
    with pytest.raises(ValueError, match="belong"):
        CompareExtractionSegments().execute(comparison(), [seg("wrong", "a1", "one", 1)], [])


def test_segment_limit_is_bounded():
    with pytest.raises(ValueError, match="limit"):
        CompareExtractionSegments(max_segments=1).execute(
            comparison(),
            [seg("run-a", "a1", "one", 1), seg("run-a", "a2", "two", 2)],
            [],
        )
