from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EndpointVerificationStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"


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
    verification_status: EndpointVerificationStatus = EndpointVerificationStatus.UNVERIFIED
    last_verified_at: datetime | None = None
    verification_note: str | None = None
