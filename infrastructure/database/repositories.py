from sqlalchemy.orm import Session
from packages.application.scenarios.repositories import ExportScenarioRepository
from packages.domain.scenario.models import ExportScenario
from infrastructure.database.models import ExportScenarioModel


class SqlAlchemyExportScenarioRepository(ExportScenarioRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, scenario: ExportScenario) -> None:
        self._session.add(ExportScenarioModel(
            id=scenario.id, product_id=scenario.product_id, hs_code=scenario.hs_code,
            origin_country_code=scenario.origin_country_code,
            destination_market_code=scenario.destination_market_code,
            scenario_date=scenario.scenario_date,
        ))
        self._session.flush()

    def get(self, scenario_id: str) -> ExportScenario | None:
        model = self._session.get(ExportScenarioModel, scenario_id)
        if model is None:
            return None
        return ExportScenario(
            id=model.id, product_id=model.product_id, hs_code=model.hs_code,
            origin_country_code=model.origin_country_code,
            destination_market_code=model.destination_market_code,
            scenario_date=model.scenario_date,
        )
