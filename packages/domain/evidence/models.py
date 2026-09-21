from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    id: str
    evidence_type: str
    source_id: str
    locator: str
    excerpt: str
    verified: bool = False
