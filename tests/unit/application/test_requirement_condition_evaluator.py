from packages.application.requirement.condition_evaluator import RequirementConditionEvaluator
from packages.domain.requirement.conditions import (
    RequirementConditionCandidate, RequirementConditionField, RequirementConditionOperator,
)
from packages.domain.requirement.evaluation import TruthValue


def condition(field, operator, value=None):
    return RequirementConditionCandidate("candidate-1", field, operator, value)


def test_missing_mandatory_fact_is_unknown():
    result = RequirementConditionEvaluator().evaluate(
        [condition(RequirementConditionField.PROCESSING_STATE, RequirementConditionOperator.EQUALS, "PROCESSED")],
        {},
    )
    assert result.result == TruthValue.UNKNOWN


def test_false_condition_is_false():
    result = RequirementConditionEvaluator().evaluate(
        [condition(RequirementConditionField.EXPORTER_TYPE, RequirementConditionOperator.EQUALS, "MANUFACTURER")],
        {"EXPORTER_TYPE": "TRADER"},
    )
    assert result.result == TruthValue.FALSE


def test_all_known_conditions_are_true():
    result = RequirementConditionEvaluator().evaluate(
        [
            condition(RequirementConditionField.EXPORTER_TYPE, RequirementConditionOperator.EQUALS, "MANUFACTURER"),
            condition(RequirementConditionField.VALUE, RequirementConditionOperator.GREATER_THAN, "1000"),
        ],
        {"EXPORTER_TYPE": "MANUFACTURER", "VALUE": 1200},
    )
    assert result.result == TruthValue.TRUE


def test_unknown_is_preserved_when_no_condition_is_false():
    result = RequirementConditionEvaluator().evaluate(
        [
            condition(RequirementConditionField.EXPORTER_TYPE, RequirementConditionOperator.EQUALS, "MANUFACTURER"),
            condition(RequirementConditionField.PROCESSING_STATE, RequirementConditionOperator.EQUALS, "PROCESSED"),
        ],
        {"EXPORTER_TYPE": "MANUFACTURER"},
    )
    assert result.result == TruthValue.UNKNOWN
