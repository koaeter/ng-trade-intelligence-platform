from packages.domain.requirement.conditions import (
    RequirementConditionCandidate, RequirementConditionField, RequirementConditionOperator,
)


class RequirementConditionCandidateService:
    def add(
        self,
        candidate_id: str,
        field: RequirementConditionField,
        operator: RequirementConditionOperator,
        value: str | None = None,
    ) -> RequirementConditionCandidate:
        if operator in {
            RequirementConditionOperator.EXISTS,
            RequirementConditionOperator.DOES_NOT_EXIST,
        } and value is not None:
            raise ValueError("Existence operators do not accept a value")
        if operator not in {
            RequirementConditionOperator.EXISTS,
            RequirementConditionOperator.DOES_NOT_EXIST,
        } and not value:
            raise ValueError("This condition operator requires a value")
        return RequirementConditionCandidate(candidate_id, field, operator, value)
