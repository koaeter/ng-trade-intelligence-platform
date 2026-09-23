from dataclasses import dataclass
from enum import Enum


class RequirementConditionField(str, Enum):
    QUANTITY = "QUANTITY"
    VALUE = "VALUE"
    EXPORTER_TYPE = "EXPORTER_TYPE"
    INTENDED_USE = "INTENDED_USE"
    PROCESSING_STATE = "PROCESSING_STATE"
    CERTIFICATE_AVAILABLE = "CERTIFICATE_AVAILABLE"
    AGREEMENT_STATUS = "AGREEMENT_STATUS"
    PREFERENCE_CLAIMED = "PREFERENCE_CLAIMED"


class RequirementConditionOperator(str, Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    IN = "IN"
    NOT_IN = "NOT_IN"
    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    LESS_THAN = "LESS_THAN"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    EXISTS = "EXISTS"
    DOES_NOT_EXIST = "DOES_NOT_EXIST"


@dataclass(frozen=True)
class RequirementConditionCandidate:
    candidate_id: str
    field: RequirementConditionField
    operator: RequirementConditionOperator
    value: str | None = None
