"""FastAPI dependency for Keycloak-protected administrative route wiring.

Import this dependency only when registering an administrative route. This module
does not register routes itself; the current API deliberately exposes no admin
write endpoints.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from packages.application.security.authorization import (
    AuthenticatedPrincipal,
    AuthorizationError,
)
from infrastructure.security.keycloak import (
    KeycloakConfigurationError,
    configured_keycloak_verifier,
)

_bearer = HTTPBearer(auto_error=False)


def get_authenticated_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> AuthenticatedPrincipal:
    """Authenticate a bearer token or return HTTP 401; never trust raw claims."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication is required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return configured_keycloak_verifier().verify(credentials.credentials)
    except (AuthorizationError, KeycloakConfigurationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or unconfigured bearer authentication",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
