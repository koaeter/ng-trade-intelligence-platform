from apps.api.main import app


def test_rule_set_administrative_write_routes_remain_unregistered():
    write_methods = {"POST", "PUT", "PATCH", "DELETE"}
    rule_set_routes = [
        route
        for route in app.routes
        if "rule-set" in getattr(route, "path", "")
        or "rule_set" in getattr(route, "path", "")
    ]

    assert all(
        not (getattr(route, "methods", set()) & write_methods)
        for route in rule_set_routes
    )
