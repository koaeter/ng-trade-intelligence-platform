from datetime import datetime, timezone

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

    def list_for_comparison(self, comparison_id: str):
        return [FakeDiff("diff-1", comparison_id)]


class FakeEntryRepository:
    def __init__(self, session) -> None:
        pass

    def list_for_diff(self, diff_id: str):
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
