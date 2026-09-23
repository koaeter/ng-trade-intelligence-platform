from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorityEndpoint:
    id: str
    authority_id: str
    url: str
    endpoint_type: str
    access_method: str = "HTTPS_WEB"
    content_format: str = "HTML"
    purpose: str | None = None
    active: bool = True
