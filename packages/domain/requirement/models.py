from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Requirement:
    id: str
    name: str
    effective_from: date
    effective_to: date | None = None
    product_ids: frozenset[str] = frozenset()
    hs_codes: frozenset[str] = frozenset()
    origin_country_codes: frozenset[str] = frozenset()
    destination_market_codes: frozenset[str] = frozenset()

    def is_effective_on(self, when: date) -> bool:
        return self.effective_from <= when and (
            self.effective_to is None or when <= self.effective_to
        )

    def scope_matches(self, product_id: str, hs_code: str, origin_country_code: str, destination_market_code: str) -> bool | None:
        checks = [
            (self.product_ids, product_id),
            (self.hs_codes, hs_code),
            (self.origin_country_codes, origin_country_code.upper()),
            (self.destination_market_codes, destination_market_code),
        ]
        if not any(values for values, _ in checks):
            return None
        return all(not values or value in values for values, value in checks)
