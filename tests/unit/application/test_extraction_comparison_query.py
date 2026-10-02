import pytest

from packages.application.source.extraction_comparison_query import GetExtractionComparison
from packages.domain.source.extraction import (
    ExtractionComparison,
    ExtractionComparisonResult,
)
from datetime import datetime, timezone


def comparison(comparison_id="cmp-1"):
    return ExtractionComparison(
        comparison_id,
        "run-a",
        "run-b",
        "input-a",
        "input-b",
        "output-a",
        "output-b",
        ExtractionComparisonResult.DIFFERENT_INPUT_DIFFERENT_OUTPUT,
        datetime(2026, 10, 2, tzinfo=timezone.utc),
    )


class ComparisonRepo:
    def __init__(self, value=None):
        self.value = value

    def get(self, comparison_id):
        return self.value if self.value and self.value.id == comparison_id else None


def test_get_returns_comparison():
    value = comparison()
    assert GetExtractionComparison(ComparisonRepo(value)).execute("cmp-1") is value


def test_missing_comparison_is_rejected():
    with pytest.raises(ValueError, match="does not exist"):
        GetExtractionComparison(ComparisonRepo()).execute("missing")
