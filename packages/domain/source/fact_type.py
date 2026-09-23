from dataclasses import dataclass


@dataclass(frozen=True)
class FactType:
    id: str
    name: str
    code: str
    description: str | None = None
    active: bool = True
