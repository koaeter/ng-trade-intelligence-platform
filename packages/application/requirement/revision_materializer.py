from packages.domain.requirement.models import Requirement


class RequirementRevisionMaterializer:
    def __init__(self, products, hs_codes, countries, markets) -> None:
        self.products = products
        self.hs_codes = hs_codes
        self.countries = countries
        self.markets = markets

    def materialize(self, revision):
        products = []
        for product_id in revision.product_ids:
            value = self.products.get(product_id)
            if value is None:
                raise ValueError(f"Missing product for requirement revision: {product_id}")
            products.append(value)

        hs_values = []
        for version_id, code in revision.hs_codes:
            value = self.hs_codes.get(version_id, code)
            if value is None:
                raise ValueError(f"Missing HS code for requirement revision: {version_id}/{code}")
            hs_values.append(value)

        countries = []
        for code in revision.origin_country_codes:
            value = self.countries.get(code)
            if value is None:
                raise ValueError(f"Missing country for requirement revision: {code}")
            countries.append(value)

        markets = []
        for code in revision.destination_market_codes:
            value = self.markets.get(code)
            if value is None:
                raise ValueError(f"Missing market for requirement revision: {code}")
            markets.append(value)

        return Requirement(
            id=revision.requirement_id,
            name=revision.name,
            effective_from=revision.effective_from,
            effective_to=revision.effective_to,
            products=frozenset(products),
            hs_codes=frozenset(hs_values),
            origin_countries=frozenset(countries),
            destination_markets=frozenset(markets),
            evidence_ids=revision.evidence_ids,
            scope_is_general=revision.scope_is_general,
        )
