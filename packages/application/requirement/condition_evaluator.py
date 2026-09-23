from collections.abc import Mapping

from packages.domain.requirement.conditions import (
    RequirementConditionCandidate, RequirementConditionOperator,
)
from packages.domain.requirement.evaluation import (
    ConditionEvaluation, ConditionSetEvaluation, TruthValue,
)


class RequirementConditionEvaluator:
    """Deterministic three-valued evaluator for structured condition candidates."""

    def evaluate(
        self,
        conditions: list[RequirementConditionCandidate],
        facts: Mapping[str, object],
    ) -> ConditionSetEvaluation:
        evaluations = tuple(self._evaluate_one(condition, facts) for condition in conditions)
        result = TruthValue.TRUE
        for item in evaluations:
            if item.result == TruthValue.FALSE:
                result = TruthValue.FALSE
                break
            if item.result == TruthValue.UNKNOWN:
                result = TruthValue.UNKNOWN
        return ConditionSetEvaluation(result, evaluations)

    def _evaluate_one(self, condition, facts):
        key = condition.field.value
        if key not in facts:
            return ConditionEvaluation(condition, TruthValue.UNKNOWN, f"Missing fact: {key}")

        actual = facts[key]
        operator = condition.operator
        expected = condition.value

        if operator == RequirementConditionOperator.EXISTS:
            return ConditionEvaluation(condition, TruthValue.TRUE, "Fact exists")
        if operator == RequirementConditionOperator.DOES_NOT_EXIST:
            return ConditionEvaluation(condition, TruthValue.FALSE, "Fact exists")

        if expected is None:
            return ConditionEvaluation(condition, TruthValue.UNKNOWN, "Expected value is missing")

        if operator in {
            RequirementConditionOperator.EQUALS,
            RequirementConditionOperator.NOT_EQUALS,
        }:
            equal = str(actual).upper() == expected.upper()
            result = equal if operator == RequirementConditionOperator.EQUALS else not equal
            return ConditionEvaluation(condition, TruthValue.TRUE if result else TruthValue.FALSE, "Equality evaluated")

        if operator in {RequirementConditionOperator.IN, RequirementConditionOperator.NOT_IN}:
            options = {item.strip().upper() for item in expected.split(",") if item.strip()}
            contained = str(actual).upper() in options
            result = contained if operator == RequirementConditionOperator.IN else not contained
            return ConditionEvaluation(condition, TruthValue.TRUE if result else TruthValue.FALSE, "Set membership evaluated")

        try:
            actual_number = float(actual)
            expected_number = float(expected)
        except (TypeError, ValueError):
            return ConditionEvaluation(condition, TruthValue.UNKNOWN, "Numeric comparison requires numeric facts")

        comparisons = {
            RequirementConditionOperator.GREATER_THAN: actual_number > expected_number,
            RequirementConditionOperator.GREATER_THAN_OR_EQUAL: actual_number >= expected_number,
            RequirementConditionOperator.LESS_THAN: actual_number < expected_number,
            RequirementConditionOperator.LESS_THAN_OR_EQUAL: actual_number <= expected_number,
        }
        result = comparisons.get(operator)
        if result is None:
            return ConditionEvaluation(condition, TruthValue.UNKNOWN, "Unsupported operator")
        return ConditionEvaluation(
            condition,
            TruthValue.TRUE if result else TruthValue.FALSE,
            "Numeric comparison evaluated",
        )
