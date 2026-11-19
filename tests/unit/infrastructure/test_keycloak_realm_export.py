import json
from pathlib import Path


def test_local_keycloak_realm_defines_api_audience_and_least_privilege_roles():
    realm_path = (
        Path(__file__).resolve().parents[3]
        / "infrastructure"
        / "keycloak"
        / "realm-export.json"
    )
    realm = json.loads(realm_path.read_text(encoding="utf-8"))

    assert realm["realm"] == "trade-intelligence"
    role_names = {role["name"] for role in realm["roles"]["realm"]}
    assert role_names == {
        "trade-admin",
        "rule-set-reader",
        "rule-set-author",
        "rule-set-validator",
        "rule-set-publisher",
        "rule-set-activator",
    }

    clients = {client["clientId"]: client for client in realm["clients"]}
    assert clients["trade-api"]["bearerOnly"] is True
    assert clients["trade-api-dev-cli"]["publicClient"] is True
    assert clients["trade-api-dev-cli"]["directAccessGrantsEnabled"] is True
    assert "trade-api-audience" in clients["trade-api-dev-cli"]["defaultClientScopes"]

    audience_mappers = [
        mapper
        for scope in realm["clientScopes"]
        for mapper in scope["protocolMappers"]
        if mapper["protocolMapper"] == "oidc-audience-mapper"
    ]
    assert any(
        mapper["config"].get("included.client.audience") == "trade-api"
        and mapper["config"].get("access.token.claim") == "true"
        for mapper in audience_mappers
    )
