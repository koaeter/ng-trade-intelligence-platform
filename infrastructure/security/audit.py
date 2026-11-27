"""Security audit events for API operations blocked by the temporary mutation lock."""
from __future__ import annotations

import json
import logging

from fastapi import Request

security_audit_logger = logging.getLogger("ng_trade_intelligence.security.audit")


def record_blocked_mutation(request: Request) -> None:
    """Emit a JSON audit event without recording sensitive request data.

    Do not log request bodies, authorization headers, cookies, query strings,
    client IPs, or other caller-controlled values.
    """
    route = request.scope.get("route")
    event = {
        "event": "mutation_blocked",
        "method": request.method,
        "route": getattr(route, "path", "<unmatched>"),
        "outcome": "denied",
        "reason": "keycloak_verification_pending",
        "http_status": 503,
        "actor": "unverified",
    }
    security_audit_logger.warning(
        json.dumps(event, sort_keys=True, separators=(",", ":")),
        extra={"security_event": event},
    )
