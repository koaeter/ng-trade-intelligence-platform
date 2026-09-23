from dataclasses import dataclass


@dataclass(frozen=True)
class RegulatoryDomain:
    id: str
    name: str
    code: str
    description: str | None = None
    parent_id: str | None = None
    active: bool = True
