from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SourceAcquisitionPolicy:
    allowed_hosts: frozenset[str]
    max_response_bytes: int = 25 * 1024 * 1024
    timeout_seconds: float = 20.0
    user_agent: str = "NG-Trade-Intelligence-Platform/1.0"


@dataclass(frozen=True)
class AcquiredSourceResponse:
    url: str
    content_type: str | None
    body: bytes


class SourceFetcher(Protocol):
    def fetch(self, url: str) -> AcquiredSourceResponse: ...
