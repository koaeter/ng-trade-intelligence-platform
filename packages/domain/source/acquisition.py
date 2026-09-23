from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AcquisitionEventStatus(str, Enum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class AcquisitionEvent:
    id: str
    source_id: str
    endpoint_id: str | None
    requested_url: str
    retrieved_url: str | None
    started_at: datetime
    completed_at: datetime
    status: AcquisitionEventStatus
    http_status: int | None
    content_type: str | None
    content_length: int | None
    response_sha256: str | None
    user_agent: str | None
    error_code: str | None = None
    error_message: str | None = None
    artifact_id: str | None = None
