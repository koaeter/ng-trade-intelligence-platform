from fastapi.testclient import TestClient

import apps.api.main as api
from apps.api.main import app


class FakeSession:
    pass


class FakeDocument:
    id = "document-1"


class FakeVersion:
    id = "version-1"
    document_id = "document-1"
    version_label = "v1"
    publication_date = None
    effective_from = None
    effective_to = None
    revision_reference = None


class FakeArtifact:
    id = "artifact-1"
    source_id = "source-1"
    document_id = "document-1"
    kind = type("Kind", (), {"value": "PDF"})()
    storage_key = "key"
    checksum_sha256 = "checksum"
    acquired_at = __import__("datetime").datetime(2026, 10, 2)
    mime_type = "application/pdf"
    original_filename = "source.pdf"
    processing_state = type("State", (), {"value": "ACQUIRED"})()
    acquisition_event_id = None
    document_version_id = "version-1"


class FakeExtraction:
    id = "extraction-1"
    artifact_id = "artifact-1"
    document_version_id = "version-1"
    input_checksum_sha256 = "checksum"
    extractor = "extractor"
    extractor_version = "1.0"
    extracted_at = __import__("datetime").datetime(2026, 10, 2)
    ocr_used = False


class FakeSegment:
    id = "segment-1"
    artifact_id = "artifact-1"
    extraction_id = "extraction-1"
    sequence = 1
    text = "text"
    page_number = 1
    section = "Section 1"
    source_start = 0
    source_end = 4
    locator = "page:1"


class FakeComparison:
    id = "comparison-1"
    baseline_extraction_id = "extraction-1"
    candidate_extraction_id = "extraction-2"
    baseline_input_checksum_sha256 = "input-1"
    candidate_input_checksum_sha256 = "input-2"
    baseline_output_sha256 = "output-1"
    candidate_output_sha256 = "output-2"
    result = type("Result", (), {"value": "DIFFERENT_INPUT_DIFFERENT_OUTPUT"})()
    compared_at = __import__("datetime").datetime(2026, 10, 2)


class FakeComparisonRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_extraction(self, extraction_id):
        return [FakeComparison()] if extraction_id == "extraction-1" else []


class FakeDiff:
    id = "diff-1"
    comparison_id = "comparison-1"
    baseline_extraction_id = "extraction-1"
    candidate_extraction_id = "extraction-2"
    entry_count = 1
    unchanged_count = 0
    added_count = 1
    removed_count = 0
    modified_count = 0
    created_at = __import__("datetime").datetime(2026, 10, 2)


class FakeDiffEntry:
    id = "diff-entry-1"
    diff_id = "diff-1"
    entry_type = type("EntryType", (), {"value": "MODIFIED"})()
    ordinal = 1
    baseline_segment_id = "segment-1"
    candidate_segment_id = "segment-2"
    baseline_sequence = 1
    candidate_sequence = 1
    baseline_text_sha256 = "old"
    candidate_text_sha256 = "new"
    baseline_page_number = 1
    candidate_page_number = 1
    baseline_section = "Section"
    candidate_section = "Section"
    baseline_source_start = 0
    baseline_source_end = 3
    candidate_source_start = 0
    candidate_source_end = 3
    baseline_locator = "page:1"
    candidate_locator = "page:1"


class FakeDiffEntryRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_diff(self, diff_id):
        return [FakeDiffEntry()] if diff_id == "diff-1" else []


class FakeDiffRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_comparison(self, comparison_id):
        return [FakeDiff()] if comparison_id == "comparison-1" else []


class FakeSegmentRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_extraction(self, extraction_id):
        return [FakeSegment()] if extraction_id == "extraction-1" else []


class FakeExtractionRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_artifact(self, artifact_id):
        return [FakeExtraction()] if artifact_id == "artifact-1" else []


class FakeRelationship:
    id = "relationship-1"
    relationship_type = type("Type", (), {"value": "SUPERSEDES"})()
    from_version_id = "version-1"
    to_version_id = "version-0"
    verified = True
    evidence_reference = "evidence-1"
    note = None


class FakeDocumentRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, document_id):
        return FakeDocument() if document_id == "document-1" else None


class FakeVersionRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_document(self, document_id):
        return [FakeVersion()] if document_id == "document-1" else []


class FakeArtifactRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_document_version(self, version_id):
        return [FakeArtifact()] if version_id == "version-1" else []


class FakeRelationshipRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_version(self, version_id):
        return [FakeRelationship()] if version_id == "version-1" else []


def test_get_document_provenance_includes_versions_artifacts_and_relationships(monkeypatch):
    monkeypatch.setattr(api, "SqlAlchemyDocumentRepository", FakeDocumentRepository)
    monkeypatch.setattr(api, "SqlAlchemyDocumentVersionRepository", FakeVersionRepository)
    monkeypatch.setattr(api, "SqlAlchemySourceArtifactRepository", FakeArtifactRepository)
    monkeypatch.setattr(api, "SqlAlchemyDocumentRelationshipRepository", FakeRelationshipRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionRunRepository", FakeExtractionRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionSegmentRepository", FakeSegmentRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionComparisonRepository", FakeComparisonRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionDiffRepository", FakeDiffRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionDiffEntryRepository", FakeDiffEntryRepository)
    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/documents/document-1/provenance")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["versions"][0]["id"] == "version-1"
    assert body["artifacts_by_version"]["version-1"][0]["id"] == "artifact-1"
    assert body["relationships_by_version"]["version-1"][0]["id"] == "relationship-1"
    assert body["extraction_runs_by_artifact"]["artifact-1"][0]["id"] == "extraction-1"
    assert body["segments_by_extraction"]["extraction-1"][0]["id"] == "segment-1"
    assert body["comparisons_by_extraction"]["extraction-1"][0]["id"] == "comparison-1"
    assert body["diffs_by_comparison"]["comparison-1"][0]["id"] == "diff-1"
    assert body["diff_entries_by_diff"]["diff-1"][0]["id"] == "diff-entry-1"


def test_get_document_provenance_returns_404_for_missing_document(monkeypatch):
    monkeypatch.setattr(api, "SqlAlchemyDocumentRepository", FakeDocumentRepository)
    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/documents/missing/provenance")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404

class FakeProvenanceSummaryRepository:
    def __init__(self, session) -> None:
        pass

    def get_summary(self, document_id):
        if document_id != "document-1":
            return None
        return type("Summary", (), {
            "document_id": "document-1",
            "version_count": 1,
            "artifact_count": 1,
            "relationship_count": 1,
            "extraction_run_count": 1,
            "segment_count": 1,
            "comparison_count": 1,
            "diff_count": 1,
            "diff_entry_count": 1,
        })()


def test_get_document_provenance_summary(monkeypatch):
    monkeypatch.setattr(
        api,
        "SqlAlchemyDocumentProvenanceSummaryRepository",
        FakeProvenanceSummaryRepository,
    )
    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/documents/document-1/provenance/summary")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["segment_count"] == 1
    assert response.json()["diff_entry_count"] == 1


def test_get_document_provenance_summary_returns_404(monkeypatch):
    monkeypatch.setattr(\n        api,\n        "SqlAlchemyDocumentProvenanceSummaryRepository",\n        FakeProvenanceSummaryRepository,\n    )
    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/documents/missing/provenance/summary")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


def test_get_document_provenance_accepts_limit_and_reports_truncation(monkeypatch):
    class LimitedArtifactRepository(FakeArtifactRepository):
        def list_for_document_version(self, version_id):
            return [
                FakeArtifact(),
                type("SecondArtifact", (), {
                    "id": "artifact-2",
                    "source_id": "source-1",
                    "document_id": "document-1",
                    "kind": type("Kind", (), {"value": "PDF"})(),
                    "storage_key": "key-2",
                    "checksum_sha256": "checksum-2",
                    "acquired_at": FakeArtifact.acquired_at,
                    "mime_type": "application/pdf",
                    "original_filename": "source-2.pdf",
                    "processing_state": type("State", (), {"value": "ACQUIRED"})(),
                    "acquisition_event_id": None,
                    "document_version_id": "version-1",
                })(),
            ]

    monkeypatch.setattr(api, "SqlAlchemyDocumentRepository", FakeDocumentRepository)
    monkeypatch.setattr(api, "SqlAlchemyDocumentVersionRepository", FakeVersionRepository)
    monkeypatch.setattr(api, "SqlAlchemySourceArtifactRepository", LimitedArtifactRepository)
    monkeypatch.setattr(api, "SqlAlchemyDocumentRelationshipRepository", FakeRelationshipRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionRunRepository", FakeExtractionRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionSegmentRepository", FakeSegmentRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionComparisonRepository", FakeComparisonRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionDiffRepository", FakeDiffRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionDiffEntryRepository", FakeDiffEntryRepository)
    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get(
            "/api/v1/documents/document-1/provenance?limit=1"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["artifacts_by_version"]["version-1"][0]["id"] == "artifact-1"
    assert "artifacts_by_version:version-1" in response.json()["truncated_collections"]
