from dataclasses import dataclass

from packages.domain.catalog.models import Country, HSCode, Market, Product
from datetime import date


@dataclass(frozen=True)
class Requirement:
    id: str
    name: str
    effective_from: date
    effective_to: date | None = None
    products: frozenset[Product] = frozenset()
    hs_codes: frozenset[HSCode] = frozenset()
    origin_countries: frozenset[Country] = frozenset()
    destination_markets: frozenset[Market] = frozenset()
    evidence_ids: tuple[str, ...] = ()
    scope_is_general: bool = False

    def is_effective_on(self, when: date) -> bool:
        return self.effective_from <= when and (
            self.effective_to is None or when <= self.effective_to
        )

    def scope_matches(self, product: Product, hs_code: HSCode, origin_country: Country, destination_market: Market) -> bool | None:
        checks = [
            (self.products, product),
            (self.hs_codes, hs_code),
            (self.origin_countries, origin_country),
            (self.destination_markets, destination_market),
        ]
        if not any(values for values, _ in checks):
            return None
        return all(not values or value in values for values, value in checks)
