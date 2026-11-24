from unittest.mock import Mock

import jwt
import pytest

from infrastructure.security.keycloak import (
    KeycloakConfigurationError,
    KeycloakTokenVerifier,
)
from packages.application.security.authorization import AuthorizationError


def verifier() -> KeycloakTokenVerifier:
    return KeycloakTokenVerifier(
        "https://identity.example/realms/trade",
        "trade-api",
        jwks_url="https://identity.example/realms/trade/protocol/openid-connect/certs",
    )


def test_keycloak_verifier_maps_explicit_realm_roles(monkeypatch):
    instance = verifier()
    instance._jwks = Mock()
    instance._jwks.get_signing_key_from_jwt.return_value.key = "public-key"
    monkeypatch.setattr(
        "infrastructure.security.keycloak.jwt.decode",
        lambda *args, **kwargs: {
            "sub": "user-123",
            "typ": "Bearer",
            "realm_access": {"roles": ["rule-set-author", "unrecognized-role"]},
            "resource_access": {},
        },
    )

    principal = instance.verify("signed-token")

    assert principal.subject == "user-123"
    assert principal.permissions == frozenset({"rule_set:read", "rule_set:draft:create"})


def test_keycloak_verifier_rejects_invalid_tokens(monkeypatch):
    instance = verifier()
    instance._jwks = Mock()
    instance._jwks.get_signing_key_from_jwt.return_value.key = "public-key"

    def reject(*args, **kwargs):
        raise jwt.InvalidTokenError("bad signature")

    monkeypatch.setattr("infrastructure.security.keycloak.jwt.decode", reject)

    with pytest.raises(AuthorizationError, match="Invalid or untrusted"):
        instance.verify("bad-token")


def test_keycloak_verifier_rejects_blank_token():
    with pytest.raises(AuthorizationError, match="Bearer token is required"):
        verifier().verify("  ")


def test_keycloak_verifier_requires_issuer_and_audience():
    with pytest.raises(KeycloakConfigurationError, match="must be configured"):
        KeycloakTokenVerifier("", "trade-api")


def test_keycloak_verifier_checks_real_signature_issuer_audience_and_expiry():
    from datetime import UTC, datetime, timedelta

    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    instance = verifier()
    instance._jwks = Mock()
    instance._jwks.get_signing_key_from_jwt.return_value.key = public_key
    now = datetime.now(UTC)

    def token(**overrides):
        claims = {
            "sub": "real-user",
            "typ": "Bearer",
            "iss": "https://identity.example/realms/trade",
            "aud": "trade-api",
            "iat": now,
            "exp": now + timedelta(minutes=5),
            "realm_access": {"roles": ["rule-set-reader"]},
        }
        claims.update(overrides)
        return jwt.encode(claims, private_key, algorithm="RS256")

    principal = instance.verify(token())
    assert principal.subject == "real-user"
    assert principal.permissions == frozenset({"rule_set:read"})

    with pytest.raises(AuthorizationError, match="Invalid or untrusted"):
        instance.verify(token(iss="https://attacker.example/realms/other"))
    with pytest.raises(AuthorizationError, match="Invalid or untrusted"):
        instance.verify(token(aud="other-api"))
    with pytest.raises(AuthorizationError, match="Invalid or untrusted"):
        instance.verify(token(exp=now - timedelta(seconds=1)))
    with pytest.raises(AuthorizationError, match="Only Keycloak access tokens"):
        instance.verify(token(typ="ID"))


def test_keycloak_verifier_fetches_jwks_and_verifies_signature_over_http():
    import json
    from datetime import UTC, datetime, timedelta
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from threading import Thread

    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(private_key.public_key()))
    public_jwk.update({"kid": "local-test-key", "use": "sig", "alg": "RS256"})
    jwks_payload = json.dumps({"keys": [public_jwk]}).encode()

    class JWKSHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(jwks_payload)

        def log_message(self, format, *args):
            return

    server = HTTPServer(("127.0.0.1", 0), JWKSHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        issuer = "https://identity.example/realms/trade"
        verifier = KeycloakTokenVerifier(
            issuer,
            "trade-api",
            jwks_url=f"http://127.0.0.1:{server.server_port}/jwks",
        )
        now = datetime.now(UTC)
        token = jwt.encode(
            {
                "sub": "jwks-user",
                "typ": "Bearer",
                "iss": issuer,
                "aud": "trade-api",
                "iat": now,
                "exp": now + timedelta(minutes=5),
                "realm_access": {"roles": ["rule-set-reader"]},
            },
            private_key,
            algorithm="RS256",
            headers={"kid": "local-test-key"},
        )

        principal = verifier.verify(token)
        assert principal.subject == "jwks-user"
        assert principal.permissions == frozenset({"rule_set:read"})
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.mark.parametrize(
    ("claim", "value", "message"),
    [
        ("realm_access", ["rule-set-reader"], "realm-role claims are malformed"),
        ("realm_access", {"roles": "rule-set-reader"}, "realm-role claims are malformed"),
        ("resource_access", ["trade-api"], "client-role claims are malformed"),
        (
            "resource_access",
            {"trade-api": ["rule-set-reader"]},
            "client-role claims are malformed",
        ),
        (
            "resource_access",
            {"trade-api": {"roles": "rule-set-reader"}},
            "client-role claims are malformed",
        ),
    ],
)
def test_keycloak_verifier_rejects_malformed_role_claim_containers(
    monkeypatch, claim, value, message
):
    instance = verifier()
    instance._jwks = Mock()
    instance._jwks.get_signing_key_from_jwt.return_value.key = "public-key"
    claims = {
        "sub": "user-123",
        "typ": "Bearer",
        "realm_access": {"roles": ["rule-set-reader"]},
        "resource_access": {},
    }
    claims[claim] = value
    monkeypatch.setattr(
        "infrastructure.security.keycloak.jwt.decode",
        lambda *args, **kwargs: claims,
    )

    with pytest.raises(AuthorizationError, match=message):
        instance.verify("signed-token")


def test_keycloak_verifier_accepts_absent_optional_role_claims(monkeypatch):
    instance = verifier()
    instance._jwks = Mock()
    instance._jwks.get_signing_key_from_jwt.return_value.key = "public-key"
    monkeypatch.setattr(
        "infrastructure.security.keycloak.jwt.decode",
        lambda *args, **kwargs: {
            "sub": "user-without-roles",
            "typ": "Bearer",
        },
    )

    principal = instance.verify("signed-token")

    assert principal.subject == "user-without-roles"
    assert principal.permissions == frozenset()
