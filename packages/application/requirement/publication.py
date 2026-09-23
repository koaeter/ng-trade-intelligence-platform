from dataclasses import dataclass
from datetime import date
from uuid import uuid4

from packages.domain.requirement.models import Requirement
from packages.domain.requirement.candidates import RequirementCandidateStatus


@dataclass(frozen=True)
class RequirementPublicationDecision:
    candidate_id: str
    reviewer_reference: str
    effective_from: date
    effective_to: date | None
    evidence_ids: tuple[str, ...]
    scope_reviewed: bool = False
    general_scope_confirmed: bool = False


class RequirementPublicationService:
    def __init__(self, candidates, scopes, requirements, products, hs_codes, countries, markets, reviews):
        self.candidates = candidates
        self.scopes = scopes
        self.requirements = requirements
        self.products = products
        self.hs_codes = hs_codes
        self.countries = countries
        self.markets = markets
        self.reviews = reviews

    def publish(self, decision: RequirementPublicationDecision) -> Requirement:
        candidate = self.candidates.get(decision.candidate_id)
        if candidate is None:
            raise ValueError("Requirement candidate does not exist")
        scope = self.scopes.get(decision.candidate_id)
        if scope is None:
            raise ValueError("Requirement scope must be reviewed before publication")
        if not decision.scope_reviewed:
            raise ValueError("Requirement scope review is required")
        if not decision.reviewer_reference.strip():
            raise ValueError("Reviewer reference is required")
        if not decision.evidence_ids:
            raise ValueError("At least one evidence reference is required")
        if decision.effective_to and decision.effective_to <= decision.effective_from:
            raise ValueError("Requirement effective_to must be after effective_from")
        if (
            not scope.product_ids
            and not scope.hs_codes
            and not scope.origin_country_codes
            and not scope.destination_market_codes
            and not decision.general_scope_confirmed
        ):
            raise ValueError("Empty scope requires explicit general-scope confirmation")

        products = []
        for product_id in scope.product_ids:
            value = self.products.get(product_id)
            if value is None:
                raise ValueError(f"Unknown product: {product_id}")
            products.append(value)

        hs_values = []
        for version_id, code in scope.hs_codes:
            value = self.hs_codes.get(version_id, code)
            if value is None:
                raise ValueError(f"Unknown HS code: {version_id}/{code}")
            hs_values.append(value)

        countries = []
        for code in scope.origin_country_codes:
            value = self.countries.get(code)
            if value is None:
                raise ValueError(f"Unknown origin country: {code}")
            countries.append(value)

        markets = []
        for code in scope.destination_market_codes:
            value = self.markets.get(code)
            if value is None:
                raise ValueError(f"Unknown destination market: {code}")
            markets.append(value)

        self.reviews.add(
            decision.candidate_id,
            decision.reviewer_reference,
            decision.scope_reviewed,
        )

        requirement = Requirement(
            id=str(uuid4()),
            name=candidate.proposed_name,
            effective_from=decision.effective_from,
            effective_to=decision.effective_to,
            products=frozenset(products),
            hs_codes=frozenset(hs_values),
            origin_countries=frozenset(countries),
            destination_markets=frozenset(markets),
            evidence_ids=tuple(decision.evidence_ids),
            scope_is_general=decision.general_scope_confirmed,
        )
        self.requirements.add(requirement)
        self.candidates.set_status(candidate.id, RequirementCandidateStatus.ACCEPTED)
        return requirement
