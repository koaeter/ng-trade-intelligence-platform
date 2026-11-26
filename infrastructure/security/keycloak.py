"""Keycloak OIDC access-token verification for administrative API dependencies.

This module validates bearer tokens and maps explicitly assigned Keycloak roles
to application permissions. Administrative route wiring remains subject to the
separate fail-closed route lock until live identity and authorization checks pass.
"""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Any
from urllib.parse import urlsplit

import jwt
from jwt import InvalidTokenError, PyJWKClient

from packages.application.security.authorization import (
    AuthenticatedPrincipal,
    AuthorizationError,
)

ROLE_PERMISSIONS: dict[str, frozenset[str]] = {
    # trade-admin is intentionally scoped to rule-set lifecycle operations.
    # It does not inherit permissions for scenarios, authority endpoints, or
    # source-catalog mutations.
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
    "scenario-creator": frozenset({"scenario:create"}),
    "scenario-evaluator": frozenset({"scenario:evaluate"}),
    "authority-endpoint-verifier": frozenset({"authority_endpoint:verify"}),
    "source-catalog-author": frozenset(
        {"source:create", "document:create", "provision:create"}
    ),
}


class KeycloakConfigurationError(RuntimeError):
    """Raised when required Keycloak verification settings are missing."""


def _validate_identity_endpoint(url: str, setting_name: str) -> None:
    """Require HTTPS for remote identity endpoints; allow HTTP only on loopback."""
    parsed = urlsplit(url)
    hostname = (parsed.hostname or "").lower()
    local_hosts = {"localhost", "127.0.0.1", "::1"}
    if (
        not hostname
        or parsed.scheme not in {"http", "https"}
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise KeycloakConfigurationError(
            f"{setting_name} must be an absolute HTTP(S) URL without credentials, "
            "query parameters, or fragments"
        )
    if parsed.scheme != "https" and hostname not in local_hosts:
        raise KeycloakConfigurationError(
            f"{setting_name} must use HTTPS unless it targets a loopback address"
        )


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
        _validate_identity_endpoint(self.issuer, "KEYCLOAK_ISSUER")
        _validate_identity_endpoint(self.jwks_url, "KEYCLOAK_JWKS_URL")
        # Use the JWKS client's bounded document cache; do not pin individual keys
        # indefinitely because Keycloak may rotate signing keys.
        self._jwks = PyJWKClient(self.jwks_url)

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

        if claims.get("typ") != "Bearer":
            raise AuthorizationError("Only Keycloak access tokens are accepted")

        subject = claims.get("sub")
        if not isinstance(subject, str) or not subject.strip():
            raise AuthorizationError("Access token has no valid subject")

        realm_access = claims.get("realm_access", {})
        if not isinstance(realm_access, dict):
            raise AuthorizationError("Access token realm-role claims are malformed")
        roles = realm_access.get("roles", [])
        if not isinstance(roles, list) or any(not isinstance(role, str) for role in roles):
            raise AuthorizationError("Access token realm-role claims are malformed")

        resource_access = claims.get("resource_access", {})
        if not isinstance(resource_access, dict):
            raise AuthorizationError("Access token client-role claims are malformed")
        client_access = resource_access.get(self.role_client_id, {})
        if not isinstance(client_access, dict):
            raise AuthorizationError("Access token client-role claims are malformed")
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
