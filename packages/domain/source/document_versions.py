from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DocumentVersion:
    """Immutable identity for one publication state/edition of a document."""
    id: str
    document_id: str
    version_label: str | None = None
    publication_date: date | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    revision_reference: str | None = None
