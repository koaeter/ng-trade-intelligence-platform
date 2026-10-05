from packages.application.source.extraction_repositories import (
    ExtractionDiffEntryRepository,
    ExtractionDiffRepository,
)
from packages.domain.source.extraction_diff import ExtractionDiff, ExtractionDiffEntry


class GetExtractionDiff:
    """Read an immutable extraction diff and its ordered entries."""

    def __init__(
        self, diffs: ExtractionDiffRepository, entries: ExtractionDiffEntryRepository
    ) -> None:
        self.diffs = diffs
        self.entries = entries

    def execute(self, diff_id: str, entry_limit: int | None = None) -> tuple[ExtractionDiff, list[ExtractionDiffEntry], bool]:
        if entry_limit is not None and entry_limit < 1:
            raise ValueError("entry_limit must be at least 1")
        diff = self.diffs.get(diff_id)
        if diff is None:
            raise ValueError("Extraction diff does not exist")
        entries = sorted(
            self.entries.list_for_diff(diff.id, limit=(entry_limit + 1 if entry_limit is not None else None)),
            key=lambda entry: entry.ordinal,
        )
        truncated = entry_limit is not None and len(entries) > entry_limit
        if entry_limit is not None:
            entries = entries[:entry_limit]
        return diff, entries, truncated


class ListExtractionDiffs:
    """List immutable extraction diffs for a comparison in repository order."""

    def __init__(self, diffs: ExtractionDiffRepository) -> None:
        self.diffs = diffs

    def execute(self, comparison_id: str, limit: int | None = None) -> list[ExtractionDiff]:
        return list(self.diffs.list_for_comparison(comparison_id, limit=limit))
