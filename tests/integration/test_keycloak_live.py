"""Opt-in integration test against a running local or test Keycloak realm."""
from __future__ import annotations

import os

import httpx
import pytest

from infrastructure.security.keycloak import KeycloakTokenVerifier


@pytest.mark.integration
def test_live_keycloak_access_token_is_verified_and_roles_are_mapped() -> None:
    issuer = os.getenv("KEYCLOAK_ISSUER", "").rstrip("/")
    username = os.getenv("KEYCLOAK_TEST_USERNAME", "")
    password = os.getenv("KEYCLOAK_TEST_PASSWORD", "")
    if not issuer or not username or not password:
        pytest.skip("Set KEYCLOAK_ISSUER and local Keycloak test-user credentials")

    token_url = f"{issuer}/protocol/openid-connect/token"
    response = httpx.post(
        token_url,
        data={
            "grant_type": "password",
            "client_id": "trade-api-dev-cli",
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
    expected_permission = os.getenv(
        "KEYCLOAK_TEST_EXPECTED_PERMISSION", "rule_set:read"
    )
    assert expected_permission in principal.permissions
