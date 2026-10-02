from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentProvenanceSummary:
    document_id: str
    version_count: int
    artifact_count: int
    relationship_count: int
    extraction_run_count: int
    segment_count: int
    comparison_count: int
    diff_count: int
    diff_entry_count: int


class GetDocumentProvenanceSummary:
    """Build a lightweight count-only document provenance summary."""

    def __init__(self, repository) -> None:
        self.repository = repository

    def execute(self, document_id: str) -> DocumentProvenanceSummary:
        summary = self.repository.get_summary(document_id)
        if summary is None:
            raise ValueError("Document not found")
        return summary
