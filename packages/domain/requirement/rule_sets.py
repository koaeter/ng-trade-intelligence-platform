from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class RuleSetStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    PUBLISHED = "PUBLISHED"
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"


@dataclass(frozen=True)
class RuleSetVersion:
    id: str
    version: str
    status: RuleSetStatus
    created_at: datetime
