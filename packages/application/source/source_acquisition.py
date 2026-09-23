from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol
from uuid import uuid4
from datetime import datetime, timezone

from packages.application.source.acquisition_repositories import AcquisitionEventRepository
from packages.domain.source.acquisition import AcquisitionEvent, AcquisitionEventStatus
from packages.domain.source.models import Source


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
    http_status: int | None = 200
    retrieved_url: str | None = None


class SourceFetcher(Protocol):
    def fetch(self, url: str) -> AcquiredSourceResponse: ...


class RegisteredSourceAcquisitionService:
    """Acquires only from a source already registered in the source registry."""

    def __init__(self, sources, events: AcquisitionEventRepository) -> None:
        self.sources = sources
        self.events = events

    def acquire(
        self,
        source_id: str,
        fetcher: SourceFetcher,
        user_agent: str | None = None,
    ) -> tuple[AcquiredSourceResponse, str]:
        source = self.sources.get(source_id)
        if source is None:
            raise ValueError("Source does not exist")
        if not source.endpoint_id:
            raise ValueError("Source is not linked to an authority endpoint")
        if not source.official_url:
            raise ValueError("Registered source has no acquisition URL")
        response, event_id = TrackedSourceAcquisitionService(self.events).acquire(
            source=source,
            fetcher=fetcher,
            url=source.official_url,
            user_agent=user_agent,
        )
        if response is None:
            raise ValueError("Successful acquisition returned no response")
        return response, event_id


class TrackedSourceAcquisitionService:
    """Fetches a registered source while persisting an auditable acquisition attempt."""

    def __init__(self, events: AcquisitionEventRepository) -> None:
        self.events = events

    def acquire(
        self,
        source: Source,
        fetcher: SourceFetcher,
        url: str | None = None,
        user_agent: str | None = None,
    ) -> tuple[AcquiredSourceResponse | None, str]:
        requested_url = url or source.official_url
        if not requested_url:
            raise ValueError("Source has no acquisition URL")
        if source.official_url and requested_url != source.official_url:
            raise ValueError("Acquisition URL does not match registered source URL")

        event_id = str(uuid4())
        started_at = datetime.now(timezone.utc)
        try:
            response = fetcher.fetch(requested_url)
            completed_at = datetime.now(timezone.utc)
            event = AcquisitionEvent(
                id=event_id,
                source_id=source.id,
                endpoint_id=source.endpoint_id,
                requested_url=requested_url,
                retrieved_url=response.retrieved_url or response.url,
                started_at=started_at,
                completed_at=completed_at,
                status=AcquisitionEventStatus.SUCCEEDED,
                http_status=response.http_status,
                content_type=response.content_type,
                content_length=len(response.body),
                response_sha256=sha256(response.body).hexdigest(),
                user_agent=user_agent,
            )
            self.events.add(event)
            return response, event_id
        except Exception as exc:
            completed_at = datetime.now(timezone.utc)
            event = AcquisitionEvent(
                id=event_id,
                source_id=source.id,
                endpoint_id=source.endpoint_id,
                requested_url=requested_url,
                retrieved_url=None,
                started_at=started_at,
                completed_at=completed_at,
                status=AcquisitionEventStatus.FAILED,
                http_status=None,
                content_type=None,
                content_length=None,
                response_sha256=None,
                user_agent=user_agent,
                error_code=type(exc).__name__,
                error_message=str(exc)[:2000] or "Source acquisition failed",
            )
            self.events.add(event)
            raise
