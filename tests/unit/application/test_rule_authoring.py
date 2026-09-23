from packages.application.requirement.rule_authoring import RequirementRuleAuthoringService
from packages.domain.requirement.conditions import (
    RequirementConditionCandidate, RequirementConditionField, RequirementConditionOperator,
)
from packages.domain.requirement.rule_set_membership import RuleSetRequirementMembership
from packages.domain.requirement.rule_tree import ConditionGroup, ConditionGroupOperator, ConditionLeaf


class Memberships:
    def list_for_rule_set(self, key):
        return [RuleSetRequirementMembership("rs1", "req-1", "req-1:r1")]


class Nodes:
    def __init__(self, existing=None):
        self.items = existing or []
    def add(self, node):
        self.items.append(node)
    def list_for_revision(self, revision_id):
        return [x for x in self.items if x.requirement_revision_id == revision_id]


def tree():
    return ConditionGroup(
        ConditionGroupOperator.AND,
        (
            ConditionLeaf(
                RequirementConditionCandidate(
                    "req-1", RequirementConditionField.VALUE,
                    RequirementConditionOperator.GREATER_THAN, "1000",
                )
            ),
        ),
    )


def test_rule_authoring_persists_revision_bound_tree():
    nodes = Nodes()
    result = RequirementRuleAuthoringService(Memberships(), nodes).add_tree(
        "rs1", "req-1", "req-1:r1", tree()
    )

    assert len(result) == 2
    assert result[0].requirement_revision_id == "req-1:r1"
    assert result[1].parent_id == result[0].id


def test_rule_authoring_does_not_mutate_an_existing_revision():
    nodes = Nodes()
    RequirementRuleAuthoringService(Memberships(), nodes).add_tree(
        "rs1", "req-1", "req-1:r1", tree()
    )
    try:
        RequirementRuleAuthoringService(Memberships(), nodes).add_tree(
            "rs1", "req-1", "req-1:r1", tree()
        )
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "new revision" in str(exc)
