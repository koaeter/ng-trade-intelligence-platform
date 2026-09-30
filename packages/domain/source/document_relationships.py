from dataclasses import dataclass
from enum import StrEnum


class DocumentRelationshipType(StrEnum):
    SUPERSEDES = "SUPERSEDES"
    AMENDS = "AMENDS"
    REPLACES = "REPLACES"
    CORRIGES = "CORRIGES"
    CONSOLIDATES = "CONSOLIDATES"
    ANNEX_OF = "ANNEX_OF"
    DERIVED_FROM = "DERIVED_FROM"


@dataclass(frozen=True)
class DocumentRelationship:
    """Explicit, reviewable relationship between two document versions."""
    id: str
    relationship_type: DocumentRelationshipType
    from_version_id: str
    to_version_id: str
    verified: bool = False
    evidence_reference: str | None = None
    note: str | None = None
