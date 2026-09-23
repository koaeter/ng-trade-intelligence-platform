from datetime import date

from packages.domain.requirement.scope_candidates import RequirementScopeCandidate


class RequirementScopeCandidateService:
    def attach(
        self,
        candidate_id: str,
        product_ids: tuple[str, ...] = (),
        hs_codes: tuple[tuple[str, str], ...] = (),
        origin_country_codes: tuple[str, ...] = (),
        destination_market_codes: tuple[str, ...] = (),
        effective_from: date | None = None,
        effective_to: date | None = None,
        conditions: tuple[str, ...] = (),
    ) -> RequirementScopeCandidate:
        if effective_from and effective_to and effective_to <= effective_from:
            raise ValueError("Requirement scope effective_to must be after effective_from")
        return RequirementScopeCandidate(
            candidate_id=candidate_id,
            product_ids=tuple(sorted(set(product_ids))),
            hs_codes=tuple(sorted(set(hs_codes))),
            origin_country_codes=tuple(sorted({x.upper() for x in origin_country_codes})),
            destination_market_codes=tuple(sorted(set(destination_market_codes))),
            effective_from=effective_from,
            effective_to=effective_to,
            conditions=tuple(sorted(set(x.strip() for x in conditions if x.strip()))),
        )
