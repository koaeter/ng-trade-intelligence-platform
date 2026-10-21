from datetime import date, datetime, UTC

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from infrastructure.database.base import Base
from infrastructure.database.models import (
    CountryModel, HSCodeModel, HSVersionModel, MarketModel, ProductModel,
    RuleSetVersionModel,
)
from infrastructure.database.repositories import (
    SqlAlchemyRequirementRepository,
    SqlAlchemyRuleSetVersionRepository,
)
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.requirement.models import Requirement
from packages.domain.requirement.rule_sets import RuleSetStatus


def test_list_all_bulk_loads_requirement_scope_and_evidence_links():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            session.add_all([
                ProductModel(id="p1", name="Cocoa"),
                HSVersionModel(id="HS2022", name="HS 2022"),
                HSCodeModel(version_id="HS2022", code="1801", description="Cocoa"),
                CountryModel(code="NG", name="Nigeria"),
                CountryModel(code="DE", name="Germany"),
                MarketModel(code="DE", name="Germany", country_code="DE"),
            ])
            session.flush()
            repo = SqlAlchemyRequirementRepository(session)
            repo.add(Requirement(
                "r1", "Scoped requirement", date(2026, 1, 1),
                products=frozenset({Product("p1", "Cocoa")}),
                hs_codes=frozenset({HSCode("HS2022", "1801", "Cocoa")}),
                origin_countries=frozenset({Country("NG", "Nigeria")}),
                destination_markets=frozenset({Market("DE", "Germany", "DE")}),
            ))
            repo.add(Requirement(
                "r2", "General requirement", date(2026, 1, 1),
                scope_is_general=True,
            ))
            session.flush()

            results = repo.list_all()

            assert [item.id for item in results] == ["r1", "r2"]
            scoped = results[0]
            assert scoped.products == frozenset({Product("p1", "Cocoa")})
            assert scoped.hs_codes == frozenset({HSCode("HS2022", "1801", "Cocoa")})
            assert scoped.origin_countries == frozenset({Country("NG", "Nigeria")})
            assert scoped.destination_markets == frozenset({Market("DE", "Germany", "DE")})
            assert scoped.evidence_ids == ()
            assert results[1].scope_is_general is True
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()



def test_rule_set_activation_retires_previous_active_version_transactionally():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            now = datetime.now(UTC)
            session.add_all([
                RuleSetVersionModel(
                    id="old", version="2026.1", status="ACTIVE", created_at=now
                ),
                RuleSetVersionModel(
                    id="new", version="2026.2", status="PUBLISHED", created_at=now
                ),
            ])
            session.flush()

            SqlAlchemyRuleSetVersionRepository(session).activate("new")

            statuses = dict(
                session.execute(
                    select(RuleSetVersionModel.id, RuleSetVersionModel.status)
                ).all()
            )
            assert statuses == {
                "old": RuleSetStatus.RETIRED.value,
                "new": RuleSetStatus.ACTIVE.value,
            }
            assert session.in_transaction()
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()
