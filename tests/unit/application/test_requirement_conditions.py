import pytest

from packages.application.requirement.conditions import RequirementConditionCandidateService
from packages.domain.requirement.conditions import (
    RequirementConditionField, RequirementConditionOperator,
)


def test_condition_candidate_requires_value_when_operator_needs_one():
    result = RequirementConditionCandidateService().add(
        "candidate-1",
        RequirementConditionField.EXPORTER_TYPE,
        RequirementConditionOperator.EQUALS,
        "MANUFACTURER",
    )
    assert result.value == "MANUFACTURER"


def test_existence_condition_has_no_value():
    result = RequirementConditionCandidateService().add(
        "candidate-1",
        RequirementConditionField.CERTIFICATE_AVAILABLE,
        RequirementConditionOperator.EXISTS,
    )
    assert result.value is None


def test_condition_rejects_missing_required_value():
    with pytest.raises(ValueError, match="requires a value"):
        RequirementConditionCandidateService().add(
            "candidate-1",
            RequirementConditionField.VALUE,
            RequirementConditionOperator.GREATER_THAN,
        )
