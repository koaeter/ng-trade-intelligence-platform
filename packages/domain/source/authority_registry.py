from dataclasses import dataclass


@dataclass(frozen=True)
class Authority:
    id: str
    name: str
    acronym: str | None
    jurisdiction_id: str
    authority_type: str
    official_url: str | None = None
    active: bool = True
