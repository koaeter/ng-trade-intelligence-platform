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


def test_get_document_provenance_returns_404_for_missing_document(monkeypatch):
    monkeypatch.setattr(api, "SqlAlchemyDocumentRepository", FakeDocumentRepository)
    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/documents/missing/provenance")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404