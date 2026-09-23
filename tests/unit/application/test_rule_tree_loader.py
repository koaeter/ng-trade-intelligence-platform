import pytest

from packages.application.requirement.rule_tree_loader import RequirementRuleTreeLoader
from packages.domain.requirement.conditions import RequirementConditionField, RequirementConditionOperator
from packages.domain.requirement.rule_nodes import RequirementRuleNode, RequirementRuleNodeType
from packages.domain.requirement.rule_tree import ConditionGroupOperator


def node(node_id, parent, sequence, node_type, **kwargs):
    return RequirementRuleNode(
        node_id, "req-1", parent, sequence, node_type, **kwargs
    )


def test_loader_builds_nested_tree():
    nodes = [
        node("root", None, 0, RequirementRuleNodeType.GROUP, group_operator=ConditionGroupOperator.AND),
        node(
            "leaf", "root", 0, RequirementRuleNodeType.CONDITION,
            field=RequirementConditionField.VALUE,
            operator=RequirementConditionOperator.GREATER_THAN,
            value="100",
        ),
    ]
    result = RequirementRuleTreeLoader().load("req-1", nodes)
    assert result.operator == ConditionGroupOperator.AND
    assert len(result.children) == 1


def test_loader_rejects_multiple_roots():
    nodes = [
        node("a", None, 0, RequirementRuleNodeType.GROUP, group_operator=ConditionGroupOperator.AND),
        node("b", None, 1, RequirementRuleNodeType.GROUP, group_operator=ConditionGroupOperator.OR),
    ]
    with pytest.raises(ValueError, match="exactly one root"):
        RequirementRuleTreeLoader().load("req-1", nodes)


def test_loader_rejects_invalid_not_group():
    nodes = [
        node("root", None, 0, RequirementRuleNodeType.GROUP, group_operator=ConditionGroupOperator.NOT),
    ]
    with pytest.raises(ValueError, match="NOT"):
        RequirementRuleTreeLoader().load("req-1", nodes)
