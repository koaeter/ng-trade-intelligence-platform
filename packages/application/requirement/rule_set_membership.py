from packages.domain.requirement.rule_set_membership import RuleSetRequirementMembership


class RuleSetMembershipService:
    def add(
        self,
        rule_set_id: str,
        requirement_id: str,
        requirement_revision: str,
    ) -> RuleSetRequirementMembership:
        if not requirement_revision.strip():
            raise ValueError("Requirement revision is required for rule-set membership")
        return RuleSetRequirementMembership(rule_set_id, requirement_id, requirement_revision)
