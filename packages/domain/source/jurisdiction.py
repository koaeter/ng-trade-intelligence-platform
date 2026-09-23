from dataclasses import dataclass
from enum import Enum


class JurisdictionType(str, Enum):
    GLOBAL = "GLOBAL"
    REGIONAL = "REGIONAL"
    COUNTRY = "COUNTRY"
    TERRITORY = "TERRITORY"
    CUSTOM = "CUSTOM"


@dataclass(frozen=True)
class Jurisdiction:
    id: str
    name: str
    jurisdiction_type: JurisdictionType
    code: str | None = None
    parent_id: str | None = None
    active: bool = True
