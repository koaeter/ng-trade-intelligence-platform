from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class RuleSetStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"


@dataclass(frozen=True)
class RuleSetVersion:
    id: str
    version: str
    status: RuleSetStatus
    created_at: datetime
