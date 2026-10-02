from packages.application.source.extraction_repositories import ExtractionComparisonRepository
from packages.domain.source.extraction import ExtractionComparison


class GetExtractionComparison:
    """Read one immutable extraction comparison."""

    def __init__(self, comparisons: ExtractionComparisonRepository) -> None:
        self.comparisons = comparisons

    def execute(self, comparison_id: str) -> ExtractionComparison:
        comparison = self.comparisons.get(comparison_id)
        if comparison is None:
            raise ValueError("Extraction comparison does not exist")
        return comparison
