from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from threading import Barrier
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from infrastructure.database.base import Base
from infrastructure.database.models import RuleSetVersionModel
from infrastructure.database.repositories import SqlAlchemyRuleSetVersionRepository


@pytest.mark.integration
def test_concurrent_rule_set_activations_preserve_single_active_invariant() -> None:
    """Competing activations may race, but exactly one must commit as ACTIVE."""
    import os

    database_url = os.getenv("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("TEST_DATABASE_URL is not configured")

    engine = create_engine(database_url, pool_size=5)
    prefix = str(uuid4())
    old_id, first_id, second_id = (
        f"{prefix}-old",
        f"{prefix}-first",
        f"{prefix}-second",
    )
    now = datetime.now(UTC)

    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            session.add_all(
                [
                    RuleSetVersionModel(
                        id=old_id,
                        version=f"{prefix}-v1",
                        status="ACTIVE",
                        created_at=now,
                    ),
                    RuleSetVersionModel(
                        id=first_id,
                        version=f"{prefix}-v2",
                        status="PUBLISHED",
                        created_at=now,
                    ),
                    RuleSetVersionModel(
                        id=second_id,
                        version=f"{prefix}-v3",
                        status="PUBLISHED",
                        created_at=now,
                    ),
                ]
            )
            session.commit()

        start_together = Barrier(2)

        def activate(version_id: str) -> str:
            with Session(engine) as session:
                start_together.wait(timeout=10)
                try:
                    SqlAlchemyRuleSetVersionRepository(session).activate(version_id)
                    session.commit()
                    return "committed"
                except IntegrityError:
                    session.rollback()
                    return "conflict"

        with ThreadPoolExecutor(max_workers=2) as executor:
            outcomes = list(executor.map(activate, (first_id, second_id)))

        assert outcomes
        assert set(outcomes) <= {"committed", "conflict"}
        assert "committed" in outcomes

        with Session(engine) as session:
            active_ids = session.scalars(
                select(RuleSetVersionModel.id).where(
                    RuleSetVersionModel.status == "ACTIVE"
                )
            ).all()
            assert len(active_ids) == 1
            assert active_ids[0] in {first_id, second_id}
    finally:
        with Session(engine) as session:
            session.query(RuleSetVersionModel).filter(
                RuleSetVersionModel.id.in_((old_id, first_id, second_id))
            ).delete(synchronize_session=False)
            session.commit()
        engine.dispose()
