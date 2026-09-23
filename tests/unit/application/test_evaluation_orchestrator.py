from datetime import date

from packages.application.scenarios.evaluation_orchestrator import ScenarioEvaluationOrchestrator
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ExportScenario


def scenario():
    return ExportScenario(
        "s1", Product("p1", "Product"), HSCode("HS2022", "1801", "Cocoa"),
        Country("NG", "Nigeria"), Market("DE", "Germany", "DE"), date(2026, 9, 21),
    )


class Scenarios:
    def get(self, key):
        return scenario() if key == "s1" else None


class Requirements:
    def list_all(self):
        return [Requirement("r1", "General requirement", date(2026, 1, 1), scope_is_general=True)]


class EvidenceRepo:
    def get(self, key):
        return Evidence("e1", "PROVISION", "src", "page=1", "evidence", True)


class RuleNodes:
    def list_for_requirement(self, key):
        return []


class Evaluations:
    def __init__(self):
        self.items = []
    def add(self, value):
        self.items.append(value)


class RuleSets:
    def get_active(self):
        class Version:
            version = "2026.09.23.1"
        return Version()


class Traces:
    def __init__(self):
        self.items = []
    def add(self, value, version):
        self.items.append((value, version))


def test_orchestrator_persists_result_and_trace():
    evaluations = Evaluations()
    traces = Traces()
    result = ScenarioEvaluationOrchestrator(
        Scenarios(), Requirements(), evaluations, EvidenceRepo(),
        RuleNodes(), traces, RuleSets(),
    ).evaluate("s1")

    assert result[0].result.value == "APPLICABLE"
    assert evaluations.items == result
    assert traces.items[0][1] == "initial"
    assert traces.items[0][0].final_result.value == "APPLICABLE"
