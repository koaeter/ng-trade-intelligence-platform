"""Inventory of legacy mutation routes pending an explicit security policy.

These assertions intentionally document exposure; they do not imply that the
routes are safe for production or protected by Keycloak.
"""
from apps.api.main import app


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
