from datetime import date

from packages.application.scenarios.deterministic_applicability import DeterministicApplicabilityService
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.conditions import RequirementConditionCandidate, RequirementConditionField, RequirementConditionOperator
from packages.domain.requirement.models import Requirement
from packages.domain.requirement.rule_tree import ConditionLeaf
from packages.domain.scenario.models import EvaluationResult, ExportScenario


def scenario():
    return ExportScenario(
        "scenario-1", Product("p1", "Product"), HSCode("HS2022", "1801", "Cocoa"),
        Country("NG", "Nigeria"), Market("DE", "Germany", "DE"), date(2026, 9, 21),
    )


def evidence():
    return (Evidence("e1", "PROVISION", "s1", "page=1", "text", True),)


def test_missing_scope_is_unresolved():
    requirement = Requirement("r1", "Requirement", date(2026, 1, 1))
    trace = DeterministicApplicabilityService().evaluate(scenario(), requirement, evidence())
    assert trace.final_result == EvaluationResult.UNRESOLVED


def test_condition_unknown_is_unresolved():
    requirement = Requirement(
        "r1", "Requirement", date(2026, 1, 1), scope_is_general=True
    )
    tree = ConditionLeaf(
        RequirementConditionCandidate(
            "r1", RequirementConditionField.PROCESSING_STATE,
            RequirementConditionOperator.EQUALS, "PROCESSED",
        )
    )
    trace = DeterministicApplicabilityService().evaluate(
        scenario(), requirement, evidence(), tree, {}
    )
    assert trace.final_result == EvaluationResult.UNRESOLVED


def test_verified_requirement_is_applicable():
    requirement = Requirement(
        "r1", "Requirement", date(2026, 1, 1), scope_is_general=True
    )
    trace = DeterministicApplicabilityService().evaluate(scenario(), requirement, evidence())
    assert trace.final_result == EvaluationResult.APPLICABLE
