"""Security audit events for API operations blocked by the temporary mutation lock."""
from __future__ import annotations

import logging

from fastapi import Request

security_audit_logger = logging.getLogger("ng_trade_intelligence.security.audit")


def record_blocked_mutation(request: Request) -> None:
    """Emit a structured, payload-free event for a rejected mutation attempt.

    Do not log request bodies, authorization headers, cookies, query strings,
    client IPs, or other caller-controlled values.
    """
    route = request.scope.get("route")
    route_template = getattr(route, "path", "<unmatched>")
    security_audit_logger.warning(
        "Mutation request blocked pending identity verification",
        extra={
            "security_event": {
                "event": "mutation_blocked",
                "method": request.method,
                "route": route_template,
                "outcome": "denied",
                "reason": "keycloak_verification_pending",
                "http_status": 503,
                "actor": "unauthenticated",
            }
        },
    )
