from packages.application.source.extraction_repositories import ExtractionRunRepository
from packages.domain.source.extraction import ExtractionRun


class GetExtractionRun:
    """Read one immutable extraction run."""

    def __init__(self, extractions: ExtractionRunRepository) -> None:
        self.extractions = extractions

    def execute(self, extraction_id: str) -> ExtractionRun:
        extraction = self.extractions.get(extraction_id)
        if extraction is None:
            raise ValueError("Extraction run does not exist")
        return extraction


class ListExtractionRunsForArtifact:
    """List immutable extraction runs for one source artifact."""

    def __init__(self, extractions: ExtractionRunRepository) -> None:
        self.extractions = extractions

    def execute(self, artifact_id: str) -> list[ExtractionRun]:
        return list(self.extractions.list_for_artifact(artifact_id))
