from fastapi.testclient import TestClient
from apps.api.main import app


def test_create_export_scenario_validation() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/export-scenarios", json={"product_id": "p", "hs_code": "1801"})
    assert response.status_code == 422


def test_scenario_date_is_required() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/export-scenarios", json={
        "product_id": "p", "hs_code": "1801", "origin_country_code": "NG",
        "destination_market_code": "DE",
    })
    assert response.status_code == 422
