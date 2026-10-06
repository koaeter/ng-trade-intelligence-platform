from fastapi.testclient import TestClient

import apps.api.main as api
from apps.api.main import app


class FakeSession:
    pass


class FakeEndpoint:
    id = "endpoint-1"
    authority_id = "authority-1"
    url = "https://example.gov.ng/api"
    endpoint_type = "API"
    access_method = "HTTPS"
    content_format = "JSON"
    purpose = "Official trade data"
    active = True
    verification_status = type("Status", (), {"value": "VERIFIED"})()
    last_verified_at = None
    verification_note = None


class FakeAuthorityEndpointRepository:
    calls = []

    def __init__(self, session) -> None:
        pass

    def list_for_authority(self, authority_id, limit=None):
        self.calls.append((authority_id, limit))
        return [FakeEndpoint()]


def test_list_authority_endpoints_passes_bounded_limit(monkeypatch):
    FakeAuthorityEndpointRepository.calls = []
    monkeypatch.setattr(api, "SqlAlchemyAuthorityEndpointRepository", FakeAuthorityEndpointRepository)
    app.dependency_overrides[api.get_session] = lambda: FakeSession()
    try:
        response = TestClient(app).get("/api/v1/authorities/authority-1/endpoints?limit=37")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()[0]["id"] == "endpoint-1"
    assert FakeAuthorityEndpointRepository.calls == [("authority-1", 37)]


def test_list_authority_endpoints_rejects_limit_above_maximum():
    response = TestClient(app).get("/api/v1/authorities/authority-1/endpoints?limit=501")
    assert response.status_code == 422
