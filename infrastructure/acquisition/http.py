from http.client import HTTPResponse
from ipaddress import ip_address
from urllib.parse import urlparse
from urllib.request import Request, build_opener

from packages.application.source.source_acquisition import (
    AcquiredSourceResponse, SourceAcquisitionPolicy,
)


class _NoRedirectHandler:
    def http_error_302(self, req, fp, code, msg, headers):
        raise ValueError("Source acquisition does not follow redirects automatically")

    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302
    http_error_308 = http_error_302


class HTTPSourceFetcher:
    """Bounded HTTPS fetcher requiring an explicit host allowlist."""

    def __init__(self, policy: SourceAcquisitionPolicy) -> None:
        self.policy = policy
        self.opener = build_opener(_NoRedirectHandler)

    def fetch(self, url: str) -> AcquiredSourceResponse:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https":
            raise ValueError("Source acquisition requires HTTPS")
        if not host or host not in {item.lower() for item in self.policy.allowed_hosts}:
            raise ValueError("Source host is not allowlisted")
        if parsed.username or parsed.password:
            raise ValueError("Source URL must not contain credentials")
        try:
            address = ip_address(host)
        except ValueError:
            address = None
        if address is not None and (address.is_private or address.is_loopback):
            raise ValueError("Private or loopback source addresses are not allowed")

        request = Request(
            url,
            headers={"User-Agent": self.policy.user_agent, "Accept": "*/*"},
            method="GET",
        )
        try:
            with self.opener.open(request, timeout=self.policy.timeout_seconds) as response:
                body = _read_bounded(response, self.policy.max_response_bytes)
                content_type = response.headers.get("Content-Type")
                return AcquiredSourceResponse(url, content_type, body)
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError("Source acquisition failed") from exc


def _read_bounded(response: HTTPResponse, maximum: int) -> bytes:
    if maximum <= 0:
        raise ValueError("Maximum response size must be positive")
    chunks: list[bytes] = []
    size = 0
    while True:
        chunk = response.read(min(1024 * 1024, maximum - size + 1))
        if not chunk:
            break
        size += len(chunk)
        if size > maximum:
            raise ValueError("Source response exceeds configured maximum")
        chunks.append(chunk)
    return b"".join(chunks)
