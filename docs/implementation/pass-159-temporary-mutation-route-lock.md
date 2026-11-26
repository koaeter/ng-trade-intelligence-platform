# Pass 159 — Fail-closed lock on legacy API mutation routes

## Decision implemented

The project owner selected Option A: temporarily disable the six legacy mutation routes until live Keycloak authentication and authorization have been verified.

## Runtime behavior

Each route now has a FastAPI dependency that raises HTTP 503 before its handler runs. The response detail is:

> Mutation endpoints are temporarily disabled pending verified Keycloak authentication and authorization.

The routes remain registered, preserving their paths and request/response definitions for future protected re-enablement. Their handler bodies are not executed, so these requests cannot create export scenarios, persist evaluations, verify and persist authority endpoint status, register sources, create documents, or create provisions.

## Routes locked

- `POST /api/v1/export-scenarios`
- `POST /api/v1/export-scenarios/{scenario_id}/evaluate`
- `POST /api/v1/authority-endpoints/{endpoint_id}/verify`
- `POST /api/v1/sources`
- `POST /api/v1/documents`
- `POST /api/v1/provisions`

Read-only routes are unchanged. The existing mutation-route inventory test remains in place, and a request-level regression test asserts that all six routes return HTTP 503 with the documented detail.

## Re-enablement gate

Do not remove the lock merely because Keycloak configuration or unit tests exist. Re-enablement requires all of the following:

1. A live Keycloak instance is available and the API validates real signed access tokens against issuer, audience, signature, expiry, and role claims.
2. Positive and negative authorization tests demonstrate that each intended role can perform only its explicitly granted operation.
3. The six data-domain operations have separately defined permissions; rule-set author permissions must not be reused as a blanket grant.
4. Audit behavior and failure handling are verified.
5. The protected route tests and CI pass, and the owner approves the resulting permission matrix.

The live Keycloak integration test remains opt-in and is not evidence of live identity-provider verification until it runs against an actual Keycloak instance with test credentials.

## Verification status

This pass adds automated API-level assertions for the fail-closed behavior. CI status is not claimed in this document; it must be checked after the commit workflow completes.
