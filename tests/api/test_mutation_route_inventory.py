"""Inventory and fail-closed behavior for legacy API mutation routes.

The routes remain registered for compatibility but reject writes until live
Keycloak authentication and authorization have been verified.
"""
import json
import logging

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


def test_all_legacy_mutation_routes_fail_closed_with_503(caplog):
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

    with caplog.at_level(
        logging.WARNING, logger="ng_trade_intelligence.security.audit"
    ):
        for method, path, payload in requests:
            response = client.request(
                method,
                path,
                json=payload,
                params={"access_token": "query-secret"},
                headers={"Authorization": "Bearer header-secret"},
            )
            assert response.status_code == 503, (path, response.text)
            assert response.json()["detail"] == MUTATIONS_DISABLED_DETAIL

    audit_records = [
        record
        for record in caplog.records
        if record.name == "ng_trade_intelligence.security.audit"
    ]
    assert len(audit_records) == len(requests)
    parsed_events = [json.loads(record.getMessage()) for record in audit_records]
    assert {event["event"] for event in parsed_events} == {"mutation_blocked"}
    assert all(event["actor"] == "unauthenticated" for event in parsed_events)
    expected_audit_fields = {
        "event", "method", "route", "outcome", "reason", "http_status", "actor"
    }
    assert all(set(event) == expected_audit_fields for event in parsed_events)
    assert {record.security_event["route"] for record in audit_records} == {
        route_path for _, route_path in EXPECTED_MUTATION_ROUTES
    }
    assert all(record.security_event["http_status"] == 503 for record in audit_records)
    assert all(record.security_event["outcome"] == "denied" for record in audit_records)
    audit_output = " ".join(record.getMessage() for record in audit_records)
    assert "Test provision" not in audit_output
    assert "query-secret" not in audit_output
    assert "header-secret" not in audit_output

    assert client.get("/health").status_code == 200
