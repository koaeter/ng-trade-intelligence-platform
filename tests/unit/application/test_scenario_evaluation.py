from datetime import date

from packages.application.scenarios.services import evaluate_requirement, evaluate_scenario
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import EvaluationResult, ExportScenario


def scenario() -> ExportScenario:
    return ExportScenario(
        "scenario-1", Product("product-1", "Product"), HSCode("HS2022", "1801", "Cocoa"),
        Country("NG", "Nigeria"), Market("DE", "Germany", "DE"), date(2026, 9, 21)
    )


def verified_evidence() -> Evidence:
    return Evidence("ev-1", "PROVISION", "src-1", "doc-1#p1", "Requirement evidence", True)


def test_active_requirement_without_evidence_is_insufficient() -> None:
    result = evaluate_requirement(scenario(), Requirement("req-1", "Sample", date(2026, 1, 1)))
    assert result.result == EvaluationResult.INSUFFICIENT_EVIDENCE


def test_active_scoped_requirement_with_verified_evidence_is_applicable() -> None:
    requirement = Requirement(
        "req-1", "Sample", date(2026, 1, 1),
        products=frozenset({Product("product-1", "Product")}),
        hs_codes=frozenset({HSCode("HS2022", "1801", "Cocoa")}),
        origin_countries=frozenset({Country("NG", "Nigeria")}),
        destination_markets=frozenset({Market("DE", "Germany", "DE")}),
        evidence_ids=("ev-1",),
    )
    result = evaluate_requirement(scenario(), requirement, (verified_evidence(),))
    assert result.result == EvaluationResult.APPLICABLE


def test_non_matching_scope_is_not_applicable() -> None:
    requirement = Requirement("req-1", "Sample", date(2026, 1, 1), hs_codes=frozenset({HSCode("HS2022", "0901", "Coffee")}))
    result = evaluate_requirement(scenario(), requirement, (verified_evidence(),))
    assert result.result == EvaluationResult.NOT_APPLICABLE


def test_unverified_evidence_is_unresolved() -> None:
    evidence = Evidence("ev-1", "PROVISION", "src-1", "doc-1#p1", "Requirement evidence", False)
    result = evaluate_requirement(scenario(), Requirement("req-1", "Sample", date(2026, 1, 1)), (evidence,))
    assert result.result == EvaluationResult.UNRESOLVED


def test_evaluate_scenario_persists_each_requirement() -> None:
    class Scenarios:
        def get(self, scenario_id: str) -> ExportScenario | None:
            return scenario() if scenario_id == "scenario-1" else None
    class Requirements:
        def list_all(self) -> list[Requirement]:
            return [Requirement("req-1", "Active", date(2026, 1, 1)), Requirement("req-2", "Future", date(2027, 1, 1))]
    class Evaluations:
        def __init__(self) -> None:
            self.items: list[object] = []
        def add(self, evaluation: object) -> None:
            self.items.append(evaluation)
    class EvidenceStore:
        def get(self, evidence_id: str) -> Evidence | None:
            return None
    evaluations = Evaluations()
    result = evaluate_scenario(Scenarios(), Requirements(), evaluations, "scenario-1", EvidenceStore())  # type: ignore[arg-type]
    assert [x.result for x in result] == [EvaluationResult.INSUFFICIENT_EVIDENCE, EvaluationResult.NOT_APPLICABLE]
    assert len(evaluations.items) == 2
