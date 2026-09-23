from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RequirementScopeCandidate:
    candidate_id: str
    product_ids: tuple[str, ...] = ()
    hs_codes: tuple[tuple[str, str], ...] = ()
    origin_country_codes: tuple[str, ...] = ()
    destination_market_codes: tuple[str, ...] = ()
    effective_from: date | None = None
    effective_to: date | None = None
    conditions: tuple[str, ...] = ()
