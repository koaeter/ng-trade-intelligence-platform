"""FastAPI dependency for Keycloak-protected administrative route wiring.

Import this dependency only when registering an administrative route. This module
does not register routes itself; the current API deliberately exposes no admin
write endpoints.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from infrastructure.security.keycloak import (
    KeycloakConfigurationError,
    configured_keycloak_verifier,
)
from packages.application.security.authorization import (
    AuthenticatedPrincipal,
    AuthorizationError,
    require_permission,
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


def require_keycloak_permission(permission: str):
    """Build a FastAPI dependency enforcing one exact application permission."""
    def dependency(
        principal: AuthenticatedPrincipal = Depends(get_authenticated_principal),
    ) -> AuthenticatedPrincipal:
        try:
            return require_permission(principal, permission)
        except AuthorizationError as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permission",
            ) from exc

    return dependency
