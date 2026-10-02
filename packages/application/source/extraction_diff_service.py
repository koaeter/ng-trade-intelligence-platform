from packages.application.source.extraction_diff import CompareExtractionSegments
from packages.application.source.extraction_repositories import (
    ExtractionComparisonRepository,
    ExtractionDiffEntryRepository,
    ExtractionDiffRepository,
    ExtractionSegmentRepository,
)
from packages.domain.source.extraction_diff import ExtractionDiff, ExtractionDiffEntry


class GenerateExtractionDiff:
    """Generate and persist a segment-level diff for an existing extraction comparison."""

    def __init__(
        self,
        comparisons: ExtractionComparisonRepository,
        segments: ExtractionSegmentRepository,
        diffs: ExtractionDiffRepository,
        entries: ExtractionDiffEntryRepository,
        comparator: CompareExtractionSegments | None = None,
    ) -> None:
        self.comparisons = comparisons
        self.segments = segments
        self.diffs = diffs
        self.entries = entries
        self.comparator = comparator or CompareExtractionSegments()

    def execute(self, comparison_id: str) -> tuple[ExtractionDiff, list[ExtractionDiffEntry]]:
        comparison = self.comparisons.get(comparison_id)
        if comparison is None:
            raise ValueError("Extraction comparison does not exist")

        baseline_segments = self.segments.list_for_extraction(
            comparison.baseline_extraction_id
        )
        candidate_segments = self.segments.list_for_extraction(
            comparison.candidate_extraction_id
        )

        diff, diff_entries = self.comparator.execute(
            comparison,
            baseline_segments,
            candidate_segments,
        )

        self.diffs.add(diff)
        for entry in diff_entries:
            self.entries.add(entry)

        return diff, diff_entries
