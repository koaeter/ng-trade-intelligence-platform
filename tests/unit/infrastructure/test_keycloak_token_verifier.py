from unittest.mock import Mock

import jwt
import pytest

from infrastructure.security.keycloak import (
    KeycloakConfigurationError,
    KeycloakTokenVerifier,
)
from packages.application.security.authorization import AuthorizationError


def verifier() -> KeycloakTokenVerifier:
    return KeycloakTokenVerifier(
        "https://identity.example/realms/trade",
        "trade-api",
        jwks_url="https://identity.example/realms/trade/protocol/openid-connect/certs",
    )


def test_keycloak_verifier_maps_explicit_realm_roles(monkeypatch):
    instance = verifier()
    instance._jwks = Mock()
    instance._jwks.get_signing_key_from_jwt.return_value.key = "public-key"
    monkeypatch.setattr(
        "infrastructure.security.keycloak.jwt.decode",
        lambda *args, **kwargs: {
            "sub": "user-123",
            "realm_access": {"roles": ["rule-set-author", "unrecognized-role"]},
            "resource_access": {},
        },
    )

    principal = instance.verify("signed-token")

    assert principal.subject == "user-123"
    assert principal.permissions == frozenset({"rule_set:read", "rule_set:draft:create"})


def test_keycloak_verifier_rejects_invalid_tokens(monkeypatch):
    instance = verifier()
    instance._jwks = Mock()
    instance._jwks.get_signing_key_from_jwt.return_value.key = "public-key"

    def reject(*args, **kwargs):
        raise jwt.InvalidTokenError("bad signature")

    monkeypatch.setattr("infrastructure.security.keycloak.jwt.decode", reject)

    with pytest.raises(AuthorizationError, match="Invalid or untrusted"):
        instance.verify("bad-token")


def test_keycloak_verifier_rejects_blank_token():
    with pytest.raises(AuthorizationError, match="Bearer token is required"):
        verifier().verify("  ")


def test_keycloak_verifier_requires_issuer_and_audience():
    with pytest.raises(KeycloakConfigurationError, match="must be configured"):
        KeycloakTokenVerifier("", "trade-api")
