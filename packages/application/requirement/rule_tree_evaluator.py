from packages.application.requirement.condition_evaluator import RequirementConditionEvaluator
from packages.domain.requirement.evaluation import TruthValue
from packages.domain.requirement.rule_tree import (
    ConditionGroup, ConditionGroupOperator, ConditionLeaf, ConditionNode,
)


class RequirementRuleTreeEvaluator:
    def __init__(self) -> None:
        self.atomic = RequirementConditionEvaluator()

    def evaluate(self, node: ConditionNode, facts):
        if isinstance(node, ConditionLeaf):
            return self.atomic.evaluate([node.condition], facts)

        child_results = tuple(self.evaluate(child, facts) for child in node.children)
        values = tuple(result.result for result in child_results)
        if node.operator == ConditionGroupOperator.AND:
            result = self._and(values)
        elif node.operator == ConditionGroupOperator.OR:
            result = self._or(values)
        else:
            if len(values) != 1:
                raise ValueError("NOT condition group requires exactly one child")
            result = self._not(values[0])
        return type(child_results[0])(
            result,
            tuple(item for child in child_results for item in child.conditions),
        ) if child_results else self.atomic.evaluate([], facts)

    @staticmethod
    def _and(values):
        if TruthValue.FALSE in values:
            return TruthValue.FALSE
        if TruthValue.UNKNOWN in values:
            return TruthValue.UNKNOWN
        return TruthValue.TRUE

    @staticmethod
    def _or(values):
        if TruthValue.TRUE in values:
            return TruthValue.TRUE
        if TruthValue.UNKNOWN in values:
            return TruthValue.UNKNOWN
        return TruthValue.FALSE

    @staticmethod
    def _not(value):
        return {
            TruthValue.TRUE: TruthValue.FALSE,
            TruthValue.FALSE: TruthValue.TRUE,
            TruthValue.UNKNOWN: TruthValue.UNKNOWN,
        }[value]
