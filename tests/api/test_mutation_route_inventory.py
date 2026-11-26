"""Inventory and fail-closed behavior for legacy API mutation routes.

The routes remain registered for compatibility but reject writes until live
Keycloak authentication and authorization have been verified.
"""
from fastapi.testclient import TestClient

from apps.api.main import MUTATIONS_DISABLED_DETAIL, app


EXPECTED_MUTATION_ROUTES = {
    ("POST", "/api/v1/export-scenarios"),
    ("POST", "/api/v1/export-scenarios/{scenario_id}/evaluate"),
    ("POST", "/api/v1/authority-endpoints/{endpoint_id}/verify"),
    ("POST", "/api/v1/sources"),
    ("POST", "/api/v1/documents"),
    ("POST", "/api/v1/provisions"),
}


def test_api_mutation_route_inventory_is_explicit_and_reviewed():
    write_methods = {"POST", "PUT", "PATCH", "DELETE"}
    actual = {
        (method, route.path)
        for route in app.routes
        for method in (getattr(route, "methods", set()) & write_methods)
    }

    assert actual == EXPECTED_MUTATION_ROUTES


def test_all_legacy_mutation_routes_fail_closed_with_503():
    client = TestClient(app)
    requests = [
        ("POST", "/api/v1/export-scenarios", {
            "product_id": "product",
            "hs_version_id": "hs-v1",
            "hs_code": "010121",
            "origin_country_code": "NG",
            "destination_market_code": "EU",
            "scenario_date": "2026-11-26",
        }),
        ("POST", "/api/v1/export-scenarios/scenario/evaluate", None),
        ("POST", "/api/v1/authority-endpoints/endpoint/verify", None),
        ("POST", "/api/v1/sources", {
            "name": "Test source",
            "organization": "Test authority",
            "source_type": "government",
            "jurisdiction": "NG",
            "endpoint_id": "endpoint",
        }),
        ("POST", "/api/v1/documents", {
            "source_id": "source",
            "title": "Test document",
            "document_type": "regulation",
        }),
        ("POST", "/api/v1/provisions", {
            "document_id": "document",
            "locator": "section 1",
            "text": "Test provision",
            "provision_type": "requirement",
        }),
    ]

    for method, path, payload in requests:
        response = client.request(method, path, json=payload)
        assert response.status_code == 503, (path, response.text)
        assert response.json()["detail"] == MUTATIONS_DISABLED_DETAIL

    assert client.get("/health").status_code == 200
