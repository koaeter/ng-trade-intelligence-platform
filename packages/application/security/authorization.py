from dataclasses import dataclass


class AuthorizationError(PermissionError):
    """Raised when an authenticated principal lacks a required permission."""


@dataclass(frozen=True)
class AuthenticatedPrincipal:
    """Identity produced only after an authentication adapter validates credentials."""

    subject: str
    permissions: frozenset[str]


def require_permission(
    principal: AuthenticatedPrincipal | None,
    permission: str,
) -> AuthenticatedPrincipal:
    """Fail closed unless a validated principal has the exact required permission."""
    if principal is None or not principal.subject.strip():
        raise AuthorizationError("Authentication is required")
    if permission not in principal.permissions:
        raise AuthorizationError(f"Missing required permission: {permission}")
    return principal
