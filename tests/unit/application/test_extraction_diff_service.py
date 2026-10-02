from datetime import datetime, timezone

import pytest

from packages.application.source.extraction_diff_service import GenerateExtractionDiff
from packages.domain.source.extraction import ExtractionComparison, ExtractionSegment
from packages.domain.source.extraction_diff import ExtractionDiffEntryType


def comparison():
    return ExtractionComparison(
        "cmp-1", "run-a", "run-b", "a" * 64, "b" * 64,
        "c" * 64, "d" * 64, "DIFFERENT_INPUT_DIFFERENT_OUTPUT",
        datetime.now(timezone.utc),
    )


def seg(run_id, segment_id, text, sequence):
    return ExtractionSegment(
        segment_id, "artifact-1", sequence, text, extraction_id=run_id
    )


class ComparisonRepo:
    def __init__(self, value): self.value = value
    def get(self, comparison_id):
        return self.value if comparison_id == self.value.id else None


class SegmentRepo:
    def __init__(self, values): self.values = values
    def list_for_extraction(self, extraction_id):
        return [x for x in self.values if x.extraction_id == extraction_id]


class DiffRepo:
    def __init__(self): self.values = []
    def add(self, diff): self.values.append(diff)


class EntryRepo:
    def __init__(self): self.values = []
    def add(self, entry): self.values.append(entry)


def service(comparison_value=None, segments=None):
    diffs = DiffRepo()
    entries = EntryRepo()
    return (
        GenerateExtractionDiff(
            ComparisonRepo(comparison_value or comparison()),
            SegmentRepo(segments or []),
            diffs,
            entries,
        ),
        diffs,
        entries,
    )


def test_persists_diff_and_entries_for_comparison():
    comparison_value = comparison()
    segments = [
        seg("run-a", "a1", "one", 1), seg("run-a", "a2", "two", 2),
        seg("run-b", "b1", "one", 1), seg("run-b", "b2", "changed", 2),
    ]
    service_value, diffs, entries = service(comparison_value, segments)
    diff, diff_entries = service_value.execute("cmp-1")
    assert diffs.values == [diff]
    assert entries.values == diff_entries
    assert [x.entry_type for x in diff_entries] == [
        ExtractionDiffEntryType.UNCHANGED, ExtractionDiffEntryType.MODIFIED,
    ]


def test_missing_comparison_is_rejected():
    service_value, diffs, entries = service(comparison())
    with pytest.raises(ValueError, match="does not exist"): service_value.execute("missing")
    assert diffs.values == []
    assert entries.values == []


def test_empty_extractions_produce_a_persisted_empty_diff():
    service_value, diffs, entries = service(comparison())
    diff, diff_entries = service_value.execute("cmp-1")
    assert diff.entry_count == 0
    assert diff_entries == []
    assert diffs.values == [diff]
    assert entries.values == []


def test_segments_are_loaded_by_extraction_run():
    comparison_value = comparison()
    segments = [
        seg("run-a", "a1", "one", 1), seg("run-b", "b1", "one", 1),
        seg("other", "x1", "should not be used", 1),
    ]
    service_value, _, _ = service(comparison_value, segments)
    diff, entries = service_value.execute("cmp-1")
    assert diff.unchanged_count == 1
    assert len(entries) == 1