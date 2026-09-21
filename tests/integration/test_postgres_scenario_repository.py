import os
from datetime import date

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from infrastructure.database.base import Base
from infrastructure.database.models import CountryModel, HSCodeModel, HSVersionModel, MarketModel, ProductModel
from infrastructure.database.repositories import SqlAlchemyApplicabilityEvaluationRepository, SqlAlchemyExportScenarioRepository, SqlAlchemyRequirementRepository
from packages.application.scenarios.services import evaluate_scenario
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ExportScenario
from packages.domain.catalog.models import Country, HSCode, Market, Product


@pytest.mark.integration
def test_postgres_scenario_evaluation_round_trip() -> None:
    database_url = os.getenv("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("TEST_DATABASE_URL is not configured")
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            session.add_all([
                ProductModel(id="product-1", name="Product"),
                HSVersionModel(id="HS2022", name="HS 2022"),
                HSCodeModel(version_id="HS2022", code="1801", description="Cocoa"),
                CountryModel(code="NG", name="Nigeria"),
                MarketModel(code="DE", name="Germany", country_code="DE"),
            ])
            session.flush()
            scenario_repo = SqlAlchemyExportScenarioRepository(session)
            requirement_repo = SqlAlchemyRequirementRepository(session)
            evaluation_repo = SqlAlchemyApplicabilityEvaluationRepository(session)
            scenario = ExportScenario("integration-evaluation-1", Product("product-1", "Product"), HSCode("HS2022", "1801", "Cocoa"), Country("NG", "Nigeria"), Market("DE", "Germany", "DE"), date(2026, 9, 21))
            requirement_repo.add(Requirement("integration-req-1", "Active requirement", date(2026, 1, 1)))
            requirement_repo.add(Requirement("integration-req-2", "Future requirement", date(2027, 1, 1)))
            scenario_repo.add(scenario)
            session.commit()
            result = evaluate_scenario(scenario_repo, requirement_repo, evaluation_repo, scenario.id)
            session.commit()
            assert len(result) == 2
            assert len(evaluation_repo.list_for_scenario(scenario.id)) == 2
    finally:
        with engine.begin() as connection:
            connection.execute(text("DROP TABLE IF EXISTS applicability_evaluations CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS requirements CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS export_scenarios CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS requirement_evidence CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS requirement_destination_markets CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS requirement_origin_countries CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS requirement_hs_codes CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS requirement_products CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS evidence CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS provisions CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS documents CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS sources CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS markets CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS countries CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS hs_codes CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS hs_versions CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS products CASCADE"))
        engine.dispose()
