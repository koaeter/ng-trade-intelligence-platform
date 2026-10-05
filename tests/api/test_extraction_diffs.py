from datetime import date, datetime, timezone

from fastapi.testclient import TestClient

import apps.api.main as api
from apps.api.main import app
from packages.domain.source.extraction_diff import ExtractionDiffEntryType


class FakeDiff:
    def __init__(self, diff_id: str, comparison_id: str) -> None:
        self.id = diff_id
        self.comparison_id = comparison_id
        self.baseline_extraction_id = "baseline"
        self.candidate_extraction_id = "candidate"
        self.entry_count = 1
        self.unchanged_count = 0
        self.added_count = 1
        self.removed_count = 0
        self.modified_count = 0
        self.created_at = datetime(2026, 10, 2, tzinfo=timezone.utc)


class FakeEntry:
    id = "entry-1"
    diff_id = "diff-1"
    entry_type = ExtractionDiffEntryType.ADDED
    ordinal = 0
    baseline_segment_id = None
    candidate_segment_id = "candidate-segment"
    baseline_sequence = None
    candidate_sequence = 2
    baseline_text_sha256 = None
    candidate_text_sha256 = "abc"
    baseline_page_number = None
    candidate_page_number = 3
    baseline_section = None
    candidate_section = "section"
    baseline_source_start = None
    baseline_source_end = None
    candidate_source_start = 10
    candidate_source_end = 20
    baseline_locator = None
    candidate_locator = "page:3"


class FakeSession:
    pass


class FakeDiffRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, diff_id: str):
        return FakeDiff(diff_id, "comparison-1") if diff_id == "diff-1" else None

    def list_for_comparison(self, comparison_id: str, limit=None):
        return [FakeDiff("diff-1", comparison_id)]


class FakeEntryRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_diff(self, diff_id: str, limit=None):
        return [FakeEntry()]


class FakeComparisonRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, comparison_id: str):
        return object() if comparison_id == "comparison-1" else None


def test_get_extraction_diff_returns_entries(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionDiffRepository", FakeDiffRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionDiffEntryRepository", FakeEntryRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/extraction-diffs/diff-1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "diff-1"
    assert body["entries"][0]["entry_type"] == "ADDED"
    assert body["entries"][0]["ordinal"] == 0
    assert body["entries_truncated"] is False


def test_get_extraction_diff_returns_404(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionDiffRepository", FakeDiffRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionDiffEntryRepository", FakeEntryRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/extraction-diffs/missing")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


def test_list_extraction_diffs_requires_existing_comparison(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionComparisonRepository", FakeComparisonRepository)
    monkeypatch.setattr(api, "SqlAlchemyExtractionDiffRepository", FakeDiffRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        found = TestClient(app).get("/api/v1/extraction-comparisons/comparison-1/diffs")
        missing = TestClient(app).get("/api/v1/extraction-comparisons/missing/diffs")
    finally:
        app.dependency_overrides.clear()

    assert found.status_code == 200
    assert found.json()[0]["comparison_id"] == "comparison-1"
    assert missing.status_code == 404


class FakeComparison:
    id = "comparison-1"
    baseline_extraction_id = "baseline"
    candidate_extraction_id = "candidate"
    baseline_input_checksum_sha256 = "input-a"
    candidate_input_checksum_sha256 = "input-b"
    baseline_output_sha256 = "output-a"
    candidate_output_sha256 = "output-b"
    result = type("Result", (), {"value": "DIFFERENT_INPUT_DIFFERENT_OUTPUT"})()
    compared_at = datetime(2026, 10, 2, tzinfo=timezone.utc)


class FakeComparisonQueryRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, comparison_id: str):
        return FakeComparison() if comparison_id == "comparison-1" else None


def test_get_extraction_comparison(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionComparisonRepository", FakeComparisonQueryRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/extraction-comparisons/comparison-1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "comparison-1"
    assert body["result"] == "DIFFERENT_INPUT_DIFFERENT_OUTPUT"


def test_get_extraction_comparison_returns_404(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionComparisonRepository", FakeComparisonQueryRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/extraction-comparisons/missing")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


class FakeRun:
    id = "run-1"
    artifact_id = "artifact-1"
    document_version_id = "version-1"
    input_checksum_sha256 = "input"
    extractor = "extractor"
    extractor_version = "1.0"
    extracted_at = datetime(2026, 10, 2, tzinfo=timezone.utc)
    ocr_used = False


class FakeRunRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, extraction_id: str):
        return FakeRun() if extraction_id == "run-1" else None


def test_get_extraction_run(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionRunRepository", FakeRunRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/extraction-runs/run-1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "run-1"
    assert body["ocr_used"] is False


def test_get_extraction_run_returns_404(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionRunRepository", FakeRunRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/extraction-runs/missing")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


class FakeSegment:
    id = "segment-1"
    artifact_id = "artifact-1"
    extraction_id = "run-1"
    sequence = 4
    text = "extracted text"
    page_number = 2
    section = "Section A"
    source_start = 10
    source_end = 24
    locator = "page:2"


class FakeSegmentRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, segment_id: str):
        return FakeSegment() if segment_id == "segment-1" else None

    def list_for_extraction(self, extraction_id: str, limit=None):
        return [FakeSegment()] if extraction_id == "run-1" else []


def test_get_extraction_segment(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionSegmentRepository", FakeSegmentRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/extraction-segments/segment-1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "segment-1"
    assert body["text"] == "extracted text"


def test_get_extraction_segment_returns_404(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionSegmentRepository", FakeSegmentRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/extraction-segments/missing")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


def test_list_extraction_segments(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionSegmentRepository", FakeSegmentRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/extraction-runs/run-1/segments")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()[0]["sequence"] == 4


class FakeArtifact:
    id = "artifact-1"
    source_id = "source-1"
    document_id = "document-1"
    kind = type("Kind", (), {"value": "PDF"})()
    storage_key = "storage/key"
    checksum_sha256 = "checksum"
    acquired_at = datetime(2026, 10, 2, tzinfo=timezone.utc)
    mime_type = "application/pdf"
    original_filename = "source.pdf"
    processing_state = type("State", (), {"value": "EXTRACTED"})()
    acquisition_event_id = "event-1"
    document_version_id = "version-1"


class FakeArtifactRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, artifact_id: str):
        return FakeArtifact() if artifact_id == "artifact-1" else None


def test_get_source_artifact(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemySourceArtifactRepository", FakeArtifactRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/source-artifacts/artifact-1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "artifact-1"
    assert body["processing_state"] == "EXTRACTED"


def test_get_source_artifact_returns_404(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemySourceArtifactRepository", FakeArtifactRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/source-artifacts/missing")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


class FakeRunListRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_artifact(self, artifact_id: str, limit=None):
        return [FakeRun()] if artifact_id == "artifact-1" else []


def test_list_extraction_runs_for_artifact(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractionRunRepository", FakeRunListRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/source-artifacts/artifact-1/extraction-runs")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()[0]["id"] == "run-1"


class FakeExtractedText:
    artifact_id = "artifact-1"
    text = "extracted text"
    extractor = "extractor"
    extractor_version = "1.0"
    extracted_at = datetime(2026, 10, 2, tzinfo=timezone.utc)
    ocr_used = True


class FakeExtractedTextRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, artifact_id: str):
        return FakeExtractedText() if artifact_id == "artifact-1" else None


def test_get_extracted_text(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractedTextRepository", FakeExtractedTextRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/source-artifacts/artifact-1/extracted-text")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["artifact_id"] == "artifact-1"
    assert body["ocr_used"] is True


def test_get_extracted_text_returns_404(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyExtractedTextRepository", FakeExtractedTextRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/source-artifacts/missing/extracted-text")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


class FakeDocumentVersion:
    id = "version-1"
    document_id = "document-1"
    version_label = "v1"
    publication_date = date(2026, 10, 1)
    effective_from = date(2026, 10, 2)
    effective_to = None
    revision_reference = "REV-1"


class FakeDocumentVersionRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, version_id: str):
        return FakeDocumentVersion() if version_id == "version-1" else None

    def list_for_document(self, document_id: str):
        return [FakeDocumentVersion()] if document_id == "document-1" else []


def test_get_document_version(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyDocumentVersionRepository", FakeDocumentVersionRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/document-versions/version-1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["version_label"] == "v1"


def test_list_document_versions(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyDocumentVersionRepository", FakeDocumentVersionRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/documents/document-1/versions")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()[0]["id"] == "version-1"


class FakeDocument:
    id = "document-1"
    source_id = "source-1"
    title = "Regulation"
    document_type = "REGULATION"
    publication_date = date(2026, 10, 1)
    effective_from = None
    effective_to = None
    version_label = "v1"


class FakeDocumentRepository:
    def __init__(self, session) -> None:
        pass

    def get(self, document_id: str):
        return FakeDocument() if document_id == "document-1" else None


def test_get_document(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyDocumentRepository", FakeDocumentRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/documents/document-1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["title"] == "Regulation"


def test_get_document_returns_404(monkeypatch) -> None:
    monkeypatch.setattr(api, "SqlAlchemyDocumentRepository", FakeDocumentRepository)

    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/documents/missing")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
