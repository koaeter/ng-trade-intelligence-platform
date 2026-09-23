from dataclasses import dataclass
from datetime import date
from enum import Enum


class AuthorityType(str, Enum):
    PRIMARY_LEGAL = "PRIMARY_LEGAL"
    OFFICIAL_INTERNATIONAL = "OFFICIAL_INTERNATIONAL"
    OFFICIAL_ADMINISTRATIVE = "OFFICIAL_ADMINISTRATIVE"
    REFERENCE_DATA = "REFERENCE_DATA"
    ANALYTICAL = "ANALYTICAL"
    SECONDARY = "SECONDARY"


class LegalEffect(str, Enum):
    BINDING = "BINDING"
    CONDITIONALLY_BINDING = "CONDITIONALLY_BINDING"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    COOPERATIVE = "COOPERATIVE"
    REFERENCE = "REFERENCE"
    INFORMATIVE = "INFORMATIVE"
    UNKNOWN = "UNKNOWN"


class InstrumentType(str, Enum):
    LAW = "LAW"
    REGULATION = "REGULATION"
    TREATY = "TREATY"
    TRADE_AGREEMENT = "TRADE_AGREEMENT"
    MOU = "MOU"
    MOA = "MOA"
    TARIFF_SCHEDULE = "TARIFF_SCHEDULE"
    OFFICIAL_NOTICE = "OFFICIAL_NOTICE"
    CIRCULAR = "CIRCULAR"
    GUIDELINE = "GUIDELINE"
    STANDARD = "STANDARD"
    PROCEDURE = "PROCEDURE"
    ADMINISTRATIVE_DECISION = "ADMINISTRATIVE_DECISION"
    OTHER = "OTHER"


@dataclass(frozen=True)
class SourceAuthorityAssignment:
    id: str
    source_id: str
    authority_type: AuthorityType
    jurisdiction: str
    domain: str
    fact_type: str
    precedence: int
    legal_weight: int
    effective_from: date | None = None
    effective_to: date | None = None
    verification_status: str = "UNVERIFIED"
    supersedes_assignment_id: str | None = None


@dataclass(frozen=True)
class Instrument:
    id: str
    document_id: str
    instrument_type: InstrumentType
    legal_effect: LegalEffect
    status: str = "ACTIVE"
    parties: tuple[str, ...] = ()
    supersedes_instrument_id: str | None = None
