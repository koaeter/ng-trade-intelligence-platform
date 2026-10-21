from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from infrastructure.security import keycloak_fastapi
from packages.application.security.authorization import (
    AuthenticatedPrincipal,
    AuthorizationError,
)


def test_fastapi_dependency_returns_401_without_bearer_credentials():
    with pytest.raises(HTTPException) as exc:
        keycloak_fastapi.get_authenticated_principal(None)
    assert exc.value.status_code == 401


def test_fastapi_dependency_maps_invalid_token_to_401(monkeypatch):
    class Verifier:
        def verify(self, token):
            raise AuthorizationError("bad token")

    monkeypatch.setattr(keycloak_fastapi, "configured_keycloak_verifier", lambda: Verifier())
    credentials = SimpleNamespace(scheme="Bearer", credentials="invalid")

    with pytest.raises(HTTPException) as exc:
        keycloak_fastapi.get_authenticated_principal(credentials)
    assert exc.value.status_code == 401


def test_permission_dependency_returns_403_for_authenticated_user_without_permission():
    dependency = keycloak_fastapi.require_keycloak_permission("rule_set:activate")
    principal = AuthenticatedPrincipal("user-1", frozenset({"rule_set:read"}))

    with pytest.raises(HTTPException) as exc:
        dependency(principal)
    assert exc.value.status_code == 403
