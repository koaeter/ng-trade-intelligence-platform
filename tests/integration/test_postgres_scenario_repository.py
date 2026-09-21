import os
from datetime import date
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from infrastructure.database.base import Base
from infrastructure.database.repositories import SqlAlchemyExportScenarioRepository
from packages.domain.scenario.models import ExportScenario


@pytest.mark.integration
def test_postgres_scenario_round_trip() -> None:
    database_url = os.getenv("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("TEST_DATABASE_URL is not configured")
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            repository = SqlAlchemyExportScenarioRepository(session)
            scenario = ExportScenario("integration-scenario-1", "product-1", "1801", "NG", "DE", date(2026, 9, 21))
            repository.add(scenario)
            session.commit()
            assert repository.get(scenario.id) == scenario
    finally:
        with engine.begin() as connection:
            connection.execute(text("DROP TABLE IF EXISTS export_scenarios CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS requirements CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS applicability_evaluations CASCADE"))
        engine.dispose()
