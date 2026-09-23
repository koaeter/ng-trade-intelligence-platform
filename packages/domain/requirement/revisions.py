from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RequirementRevision:
    id: str
    requirement_id: str
    revision: str
    name: str
    effective_from: date
    effective_to: date | None
    product_ids: tuple[str, ...]
    hs_codes: tuple[tuple[str, str], ...]
    origin_country_codes: tuple[str, ...]
    destination_market_codes: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    scope_is_general: bool
