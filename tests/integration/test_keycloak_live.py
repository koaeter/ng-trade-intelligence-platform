"""Opt-in integration test against a running local or remote test Keycloak realm."""
from __future__ import annotations

import os
from urllib.parse import urlparse

import httpx
import pytest

from infrastructure.security.keycloak import KeycloakTokenVerifier


def _validate_issuer_transport(issuer: str) -> None:
    """Never transmit test-user credentials to an insecure or malformed issuer."""
    parsed = urlparse(issuer)
    hostname = (parsed.hostname or "").lower()
    local_hosts = {"localhost", "127.0.0.1", "::1"}
    if not hostname or parsed.scheme not in {"http", "https"}:
        raise ValueError("KEYCLOAK_ISSUER must be an absolute HTTP(S) URL")
    if parsed.scheme != "https" and hostname not in local_hosts:
        raise ValueError(
            "KEYCLOAK_ISSUER must use HTTPS unless it targets a loopback address"
        )


@pytest.mark.parametrize(
    ("issuer", "should_raise"),
    [
        ("https://identity.example/realms/trade", False),
        ("http://localhost:8081/realms/trade", False),
        ("http://127.0.0.1:8081/realms/trade", False),
        ("http://identity.example/realms/trade", True),
        ("ftp://identity.example/realms/trade", True),
        ("https:///realms/trade", True),
    ],
)
def test_live_keycloak_issuer_requires_valid_secure_transport(issuer, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            _validate_issuer_transport(issuer)
    else:
        _validate_issuer_transport(issuer)


@pytest.mark.integration
def test_live_keycloak_access_token_is_verified_and_roles_are_mapped() -> None:
    issuer = os.getenv("KEYCLOAK_ISSUER", "").rstrip("/")
    username = os.getenv("KEYCLOAK_TEST_USERNAME", "")
    password = os.getenv("KEYCLOAK_TEST_PASSWORD", "")
    if not issuer or not username or not password:
        pytest.skip("Set KEYCLOAK_ISSUER and test-user credentials")

    _validate_issuer_transport(issuer)
    token_url = f"{issuer}/protocol/openid-connect/token"
    response = httpx.post(
        token_url,
        data={
            "grant_type": "password",
            "client_id": os.getenv("KEYCLOAK_TEST_CLIENT_ID", "trade-api-dev-cli"),
            "username": username,
            "password": password,
        },
        timeout=15.0,
    )
    response.raise_for_status()
    access_token = response.json()["access_token"]

    verifier = KeycloakTokenVerifier(
        issuer,
        os.getenv("KEYCLOAK_AUDIENCE", "trade-api"),
        jwks_url=os.getenv("KEYCLOAK_JWKS_URL") or None,
        role_client_id=os.getenv("KEYCLOAK_ROLE_CLIENT_ID", "trade-api"),
    )
    principal = verifier.verify(access_token)

    assert principal.subject
    expected_permissions = {
        item.strip()
        for item in os.getenv(
            "KEYCLOAK_TEST_EXPECTED_PERMISSIONS",
            os.getenv("KEYCLOAK_TEST_EXPECTED_PERMISSION", "rule_set:read"),
        ).split(",")
        if item.strip()
    }
    forbidden_permissions = {
        item.strip()
        for item in os.getenv("KEYCLOAK_TEST_FORBIDDEN_PERMISSIONS", "").split(",")
        if item.strip()
    }

    assert expected_permissions <= principal.permissions
    assert forbidden_permissions.isdisjoint(principal.permissions)
