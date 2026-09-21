from datetime import date
from packages.application.scenarios.services import create_scenario, get_scenario
from packages.domain.scenario.models import ExportScenario


class InMemoryScenarioRepository:
    def __init__(self) -> None:
        self.items: dict[str, ExportScenario] = {}
    def add(self, scenario: ExportScenario) -> None:
        self.items[scenario.id] = scenario
    def get(self, scenario_id: str) -> ExportScenario | None:
        return self.items.get(scenario_id)


def test_application_service_uses_repository_boundary() -> None:
    repository = InMemoryScenarioRepository()
    scenario = ExportScenario("scenario-1", "product-1", "1801", "NG", "DE", date(2026, 9, 21))
    create_scenario(repository, scenario)  # type: ignore[arg-type]
    assert get_scenario(repository, "scenario-1") == scenario  # type: ignore[arg-type]
