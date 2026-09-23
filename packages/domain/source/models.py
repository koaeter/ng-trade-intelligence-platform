from dataclasses import dataclass
from datetime import date
from enum import Enum


class SourceStatus(str, Enum):
    DISCOVERED = "DISCOVERED"
    ACQUIRED = "ACQUIRED"
    EXTRACTED = "EXTRACTED"
    CANDIDATE = "CANDIDATE"
    REVIEWED = "REVIEWED"
    PUBLISHED = "PUBLISHED"
    SUPERSEDED = "SUPERSEDED"
    RETIRED = "RETIRED"


@dataclass(frozen=True)
class Source:
    id: str
    name: str
    organization: str
    source_type: str
    jurisdiction: str | None = None
    official_url: str | None = None
    status: SourceStatus = SourceStatus.DISCOVERED
    endpoint_id: str | None = None


@dataclass(frozen=True)
class Document:
    id: str
    source_id: str
    title: str
    document_type: str
    publication_date: date | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    version_label: str | None = None


@dataclass(frozen=True)
class Provision:
    id: str
    document_id: str
    locator: str
    text: str
    provision_type: str
