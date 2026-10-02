from difflib import SequenceMatcher
from hashlib import sha256
from uuid import uuid4
from datetime import datetime, timezone

from packages.domain.source.extraction import ExtractionComparison, ExtractionSegment
from packages.domain.source.extraction_diff import (
    ExtractionDiff,
    ExtractionDiffEntry,
    ExtractionDiffEntryType,
)


class CompareExtractionSegments:
    """Create a deterministic, immutable segment-level diff."""

    def __init__(self, max_segments: int = 10_000) -> None:
        if max_segments < 1:
            raise ValueError("max_segments must be positive")
        self.max_segments = max_segments

    def execute(
        self,
        comparison: ExtractionComparison,
        baseline_segments: list[ExtractionSegment],
        candidate_segments: list[ExtractionSegment],
    ) -> tuple[ExtractionDiff, list[ExtractionDiffEntry]]:
        self._validate_segments(baseline_segments, comparison.baseline_extraction_id)
        self._validate_segments(candidate_segments, comparison.candidate_extraction_id)

        baseline = sorted(baseline_segments, key=lambda x: (x.sequence, x.id))
        candidate = sorted(candidate_segments, key=lambda x: (x.sequence, x.id))

        diff_id = str(uuid4())
        entries: list[ExtractionDiffEntry] = []
        ordinal = 0

        matcher = SequenceMatcher(
            a=[segment.text for segment in baseline],
            b=[segment.text for segment in candidate],
            autojunk=False,
        )

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                for left, right in zip(baseline[i1:i2], candidate[j1:j2]):
                    entries.append(self._entry(
                        diff_id, ordinal, ExtractionDiffEntryType.UNCHANGED, left, right
                    ))
                    ordinal += 1
            elif tag == "replace":
                left_block = baseline[i1:i2]
                right_block = candidate[j1:j2]
                paired = min(len(left_block), len(right_block))
                for offset in range(paired):
                    entries.append(self._entry(
                        diff_id, ordinal, ExtractionDiffEntryType.MODIFIED,
                        left_block[offset], right_block[offset],
                    ))
                    ordinal += 1
                for left in left_block[paired:]:
                    entries.append(self._entry(
                        diff_id, ordinal, ExtractionDiffEntryType.REMOVED, left, None
                    ))
                    ordinal += 1
                for right in right_block[paired:]:
                    entries.append(self._entry(
                        diff_id, ordinal, ExtractionDiffEntryType.ADDED, None, right
                    ))
                    ordinal += 1
            elif tag == "delete":
                for left in baseline[i1:i2]:
                    entries.append(self._entry(
                        diff_id, ordinal, ExtractionDiffEntryType.REMOVED, left, None
                    ))
                    ordinal += 1
            elif tag == "insert":
                for right in candidate[j1:j2]:
                    entries.append(self._entry(
                        diff_id, ordinal, ExtractionDiffEntryType.ADDED, None, right
                    ))
                    ordinal += 1
            else:
                raise ValueError(f"Unsupported diff opcode: {tag}")

        counts = {
            kind: sum(1 for entry in entries if entry.entry_type == kind)
            for kind in ExtractionDiffEntryType
        }
        diff = ExtractionDiff(
            id=diff_id,
            comparison_id=comparison.id,
            baseline_extraction_id=comparison.baseline_extraction_id,
            candidate_extraction_id=comparison.candidate_extraction_id,
            entry_count=len(entries),
            unchanged_count=counts[ExtractionDiffEntryType.UNCHANGED],
            added_count=counts[ExtractionDiffEntryType.ADDED],
            removed_count=counts[ExtractionDiffEntryType.REMOVED],
            modified_count=counts[ExtractionDiffEntryType.MODIFIED],
            created_at=datetime.now(timezone.utc),
        )
        return diff, entries

    def _validate_segments(
        self,
        segments: list[ExtractionSegment],
        extraction_id: str,
    ) -> None:
        if len(segments) > self.max_segments:
            raise ValueError(f"Extraction segment count exceeds limit of {self.max_segments}")
        for segment in segments:
            if segment.extraction_id != extraction_id:
                raise ValueError("All segments must belong to the compared extraction run")

    @staticmethod
    def _text_hash(text: str | None) -> str | None:
        return None if text is None else sha256(text.encode("utf-8")).hexdigest()

    def _entry(
        self,
        diff_id: str,
        ordinal: int,
        entry_type: ExtractionDiffEntryType,
        baseline: ExtractionSegment | None,
        candidate: ExtractionSegment | None,
    ) -> ExtractionDiffEntry:
        return ExtractionDiffEntry(
            id=f"{diff_id}:entry:{ordinal}",
            diff_id=diff_id,
            entry_type=entry_type,
            ordinal=ordinal,
            baseline_segment_id=baseline.id if baseline else None,
            candidate_segment_id=candidate.id if candidate else None,
            baseline_sequence=baseline.sequence if baseline else None,
            candidate_sequence=candidate.sequence if candidate else None,
            baseline_text_sha256=self._text_hash(baseline.text if baseline else None),
            candidate_text_sha256=self._text_hash(candidate.text if candidate else None),
            baseline_page_number=baseline.page_number if baseline else None,
            candidate_page_number=candidate.page_number if candidate else None,
            baseline_section=baseline.section if baseline else None,
            candidate_section=candidate.section if candidate else None,
            baseline_source_start=baseline.source_start if baseline else None,
            baseline_source_end=baseline.source_end if baseline else None,
            candidate_source_start=candidate.source_start if candidate else None,
            candidate_source_end=candidate.source_end if candidate else None,
            baseline_locator=baseline.locator if baseline else None,
            candidate_locator=candidate.locator if candidate else None,
        )
