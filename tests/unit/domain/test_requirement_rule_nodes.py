from packages.domain.requirement.conditions import (
    RequirementConditionField, RequirementConditionOperator,
)
from packages.domain.requirement.rule_nodes import RequirementRuleNode, RequirementRuleNodeType
from packages.domain.requirement.rule_tree import ConditionGroupOperator


def test_rule_node_can_represent_condition_leaf():
    node = RequirementRuleNode(
        "node-1", "req-1", None, 0, RequirementRuleNodeType.CONDITION,
        field=RequirementConditionField.VALUE,
        operator=RequirementConditionOperator.GREATER_THAN,
        value="1000",
    )
    assert node.node_type == RequirementRuleNodeType.CONDITION
    assert node.parent_id is None


def test_rule_node_can_represent_group():
    node = RequirementRuleNode(
        "node-1", "req-1", None, 0, RequirementRuleNodeType.GROUP,
        group_operator=ConditionGroupOperator.AND,
    )
    assert node.group_operator == ConditionGroupOperator.AND
