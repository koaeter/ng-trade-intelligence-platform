from packages.application.requirement.revision_materializer import RequirementRevisionMaterializer
from packages.application.requirement.rule_tree_loader import RequirementRuleTreeLoader


class RuleSetPublicationValidator:
    def __init__(self, memberships, revisions, rule_nodes, products, hs_codes, countries, markets):
        self.memberships = memberships
        self.revisions = revisions
        self.rule_nodes = rule_nodes
        self.materializer = RequirementRevisionMaterializer(
            products, hs_codes, countries, markets
        )
        self.loader = RequirementRuleTreeLoader()

    def validate(self, rule_set_id: str) -> None:
        memberships = self.memberships.list_for_rule_set(rule_set_id)
        if not memberships:
            raise ValueError("Rule set contains no requirement memberships")

        for membership in memberships:
            revision = self.revisions.get(membership.requirement_revision)
            if revision is None:
                raise ValueError(
                    f"Rule set references missing requirement revision: "
                    f"{membership.requirement_revision}"
                )
            if revision.requirement_id != membership.requirement_id:
                raise ValueError("Rule-set membership and requirement revision disagree")

            self.materializer.materialize(revision)
            nodes = self.rule_nodes.list_for_requirement(revision.requirement_id)
            if nodes:
                self.loader.load(revision.requirement_id, revision.id, nodes)
