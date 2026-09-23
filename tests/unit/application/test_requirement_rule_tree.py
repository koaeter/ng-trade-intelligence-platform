from packages.application.requirement.rule_tree_evaluator import RequirementRuleTreeEvaluator
from packages.domain.requirement.conditions import (
    RequirementConditionCandidate, RequirementConditionField, RequirementConditionOperator,
)
from packages.domain.requirement.evaluation import TruthValue
from packages.domain.requirement.rule_tree import ConditionGroup, ConditionGroupOperator, ConditionLeaf


def leaf(field, value):
    return ConditionLeaf(
        RequirementConditionCandidate(
            "candidate-1", field, RequirementConditionOperator.EQUALS, value
        )
    )


def test_and_group_preserves_unknown():
    node = ConditionGroup(
        ConditionGroupOperator.AND,
        (
            leaf(RequirementConditionField.EXPORTER_TYPE, "MANUFACTURER"),
            leaf(RequirementConditionField.PROCESSING_STATE, "PROCESSED"),
        ),
    )
    result = RequirementRuleTreeEvaluator().evaluate(
        node, {"EXPORTER_TYPE": "MANUFACTURER"}
    )
    assert result.result == TruthValue.UNKNOWN


def test_or_group_returns_true_when_any_branch_is_true():
    node = ConditionGroup(
        ConditionGroupOperator.OR,
        (
            leaf(RequirementConditionField.EXPORTER_TYPE, "MANUFACTURER"),
            leaf(RequirementConditionField.EXPORTER_TYPE, "TRADER"),
        ),
    )
    result = RequirementRuleTreeEvaluator().evaluate(node, {"EXPORTER_TYPE": "TRADER"})
    assert result.result == TruthValue.TRUE


def test_not_group_inverts_known_result():
    node = ConditionGroup(
        ConditionGroupOperator.NOT,
        (leaf(RequirementConditionField.EXPORTER_TYPE, "MANUFACTURER"),),
    )
    result = RequirementRuleTreeEvaluator().evaluate(
        node, {"EXPORTER_TYPE": "TRADER"}
    )
    assert result.result == TruthValue.TRUE
