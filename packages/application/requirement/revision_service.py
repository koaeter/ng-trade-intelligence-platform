from packages.domain.requirement.models import Requirement
from packages.domain.requirement.revisions import RequirementRevision


class RequirementRevisionService:
    def snapshot(self, requirement: Requirement, revision: str) -> RequirementRevision:
        if not revision.strip():
            raise ValueError("Requirement revision is required")
        return RequirementRevision(
            id=f"{requirement.id}:{revision}",
            requirement_id=requirement.id,
            revision=revision,
            name=requirement.name,
            effective_from=requirement.effective_from,
            effective_to=requirement.effective_to,
            product_ids=tuple(sorted(x.id for x in requirement.products)),
            hs_codes=tuple(sorted((x.version_id, x.code) for x in requirement.hs_codes)),
            origin_country_codes=tuple(sorted(x.code for x in requirement.origin_countries)),
            destination_market_codes=tuple(sorted(x.code for x in requirement.destination_markets)),
            evidence_ids=tuple(requirement.evidence_ids),
            scope_is_general=requirement.scope_is_general,
        )
