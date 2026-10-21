"""Keycloak OIDC access-token verification for administrative API dependencies.

This module validates bearer tokens but intentionally does not expose or register
administrative endpoints. Route wiring must remain disabled until deployment
configuration and integration tests are verified.
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import jwt
from jwt import InvalidTokenError, PyJWKClient

from packages.application.security.authorization import (
    AuthenticatedPrincipal,
    AuthorizationError,
)

ROLE_PERMISSIONS: dict[str, frozenset[str]] = {
    "trade-admin": frozenset(
        {
            "rule_set:read",
            "rule_set:draft:create",
            "rule_set:validate",
            "rule_set:publish",
            "rule_set:activate",
        }
    ),
    "rule-set-reader": frozenset({"rule_set:read"}),
    "rule-set-author": frozenset({"rule_set:read", "rule_set:draft:create"}),
    "rule-set-validator": frozenset({"rule_set:read", "rule_set:validate"}),
    "rule-set-publisher": frozenset({"rule_set:read", "rule_set:publish"}),
    "rule-set-activator": frozenset({"rule_set:read", "rule_set:activate"}),
}


class KeycloakConfigurationError(RuntimeError):
    """Raised when required Keycloak verification settings are missing."""


class KeycloakTokenVerifier:
    """Verify Keycloak-signed access tokens and map realm roles to permissions."""

    def __init__(
        self,
        issuer: str,
        audience: str,
        *,
        jwks_url: str | None = None,
        role_client_id: str | None = None,
    ) -> None:
        self.issuer = issuer.rstrip("/")
        self.audience = audience.strip()
        if not self.issuer or not self.audience:
            raise KeycloakConfigurationError(
                "KEYCLOAK_ISSUER and KEYCLOAK_AUDIENCE must be configured"
            )
        self.role_client_id = role_client_id or self.audience
        self.jwks_url = jwks_url or f"{self.issuer}/protocol/openid-connect/certs"
        self._jwks = PyJWKClient(self.jwks_url, cache_keys=True)

    def verify(self, token: str) -> AuthenticatedPrincipal:
        """Return a trusted principal only after signature and claim validation."""
        if not token.strip():
            raise AuthorizationError("Bearer token is required")
        try:
            signing_key = self._jwks.get_signing_key_from_jwt(token)
            claims: dict[str, Any] = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
                options={"require": ["exp", "iat", "sub", "iss", "aud"]},
            )
        except (InvalidTokenError, jwt.PyJWKClientError, ValueError) as exc:
            raise AuthorizationError("Invalid or untrusted access token") from exc

        subject = claims.get("sub")
        if not isinstance(subject, str) or not subject.strip():
            raise AuthorizationError("Access token has no valid subject")

        realm_access = claims.get("realm_access")
        roles = realm_access.get("roles", []) if isinstance(realm_access, dict) else []
        if not isinstance(roles, list) or any(not isinstance(role, str) for role in roles):
            raise AuthorizationError("Access token role claims are malformed")

        resource_access = claims.get("resource_access", {})
        client_roles: list[str] = []
        if isinstance(resource_access, dict):
            client_access = resource_access.get(self.role_client_id, {})
            if isinstance(client_access, dict):
                client_roles = client_access.get("roles", [])
        if not isinstance(client_roles, list) or any(
            not isinstance(role, str) for role in client_roles
        ):
            raise AuthorizationError("Access token client-role claims are malformed")

        permissions = frozenset(
            permission
            for role in set(roles + client_roles)
            for permission in ROLE_PERMISSIONS.get(role, frozenset())
        )
        return AuthenticatedPrincipal(subject=subject, permissions=permissions)


@lru_cache(maxsize=1)
def configured_keycloak_verifier() -> KeycloakTokenVerifier:
    """Build the verifier from environment configuration; fail closed if absent."""
    issuer = os.environ.get("KEYCLOAK_ISSUER", "")
    audience = os.environ.get("KEYCLOAK_AUDIENCE", "")
    jwks_url = os.environ.get("KEYCLOAK_JWKS_URL") or None
    role_client_id = os.environ.get("KEYCLOAK_ROLE_CLIENT_ID") or None
    return KeycloakTokenVerifier(
        issuer,
        audience,
        jwks_url=jwks_url,
        role_client_id=role_client_id,
    )
