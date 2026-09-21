from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    id: str
    evidence_type: str
    source_id: str
    locator: str
    excerpt: str
    verified: bool = False
    document_id: str | None = None
    provision_id: str | None = None
