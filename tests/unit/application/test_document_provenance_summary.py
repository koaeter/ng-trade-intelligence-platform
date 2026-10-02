from packages.application.source.document_provenance_summary import GetDocumentProvenanceSummary


class MemorySummaryRepository:
    def __init__(self, summary):
        self.summary = summary

    def get_summary(self, document_id):
        return self.summary if document_id == "document-1" else None


def test_get_document_provenance_summary_returns_repository_summary():
    summary = type("Summary", (), {"document_id": "document-1", "version_count": 2, "artifact_count": 3,
        "relationship_count": 1, "extraction_run_count": 4, "segment_count": 100,
        "comparison_count": 2, "diff_count": 2, "diff_entry_count": 12})()
    result = GetDocumentProvenanceSummary(MemorySummaryRepository(summary)).execute("document-1")
    assert result.document_id == "document-1"
    assert result.version_count == 2
    assert result.segment_count == 100
    assert result.diff_entry_count == 12


def test_get_document_provenance_summary_rejects_missing_document():
    repository = MemorySummaryRepository(None)
    try:
        GetDocumentProvenanceSummary(repository).execute("missing")
    except ValueError as exc:
        assert str(exc) == "Document not found"
    else:
        raise AssertionError("expected ValueError")
