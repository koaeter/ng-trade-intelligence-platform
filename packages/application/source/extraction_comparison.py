from hashlib import sha256
from uuid import uuid4
from datetime import datetime, timezone

from packages.domain.source.extraction import (
    ExtractionComparison,
    ExtractionComparisonResult,
    ExtractionRun,
    ExtractionSegment,
)


class CompareExtractionRuns:
    """Compare two immutable extraction runs without modifying either run."""

    def execute(
        self,
        baseline: ExtractionRun,
        candidate: ExtractionRun,
        baseline_segments: list[ExtractionSegment],
        candidate_segments: list[ExtractionSegment],
    ) -> ExtractionComparison:
        if baseline.id == candidate.id:
            raise ValueError("An extraction run cannot be compared with itself")
        if baseline.artifact_id != candidate.artifact_id:
            raise ValueError("Extraction runs must belong to the same artifact")
        if baseline.input_checksum_sha256 != candidate.input_checksum_sha256:
            result = ExtractionComparisonResult.DIFFERENT_INPUT_DIFFERENT_OUTPUT
        else:
            result = (
                ExtractionComparisonResult.SAME_INPUT_SAME_OUTPUT
                if self._output_hash(baseline_segments) == self._output_hash(candidate_segments)
                else ExtractionComparisonResult.SAME_INPUT_DIFFERENT_OUTPUT
            )
        return ExtractionComparison(
            id=str(uuid4()),
            baseline_extraction_id=baseline.id,
            candidate_extraction_id=candidate.id,
            baseline_input_checksum_sha256=baseline.input_checksum_sha256,
            candidate_input_checksum_sha256=candidate.input_checksum_sha256,
            baseline_output_sha256=self._output_hash(baseline_segments),
            candidate_output_sha256=self._output_hash(candidate_segments),
            result=result,
            compared_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _output_hash(segments: list[ExtractionSegment]) -> str:
        ordered = sorted(segments, key=lambda x: (x.sequence, x.id))
        payload = "\n".join(segment.text for segment in ordered).encode("utf-8")
        return sha256(payload).hexdigest()
