from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from infrastructure.database.base import Base
from infrastructure.database.models import RuleSetAuditEventModel, RuleSetVersionModel
from infrastructure.database.repositories import SqlAlchemyRuleSetAuditRepository


def test_rule_set_audit_event_records_actor_action_target_and_time():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            session.add(
                RuleSetVersionModel(
                    id="rs-1",
                    version="2026.11",
                    status="PUBLISHED",
                    created_at=datetime(2026, 10, 21, tzinfo=UTC),
                )
            )
            session.flush()
            occurred_at = datetime(2026, 10, 21, 9, 30, tzinfo=UTC)
            event_id = SqlAlchemyRuleSetAuditRepository(session).record(
                actor_subject="keycloak-subject-123",
                action="activate",
                target_rule_set_id="rs-1",
                outcome="SUCCEEDED",
                detail="Activated after validation",
                occurred_at=occurred_at,
            )

            event = session.get(RuleSetAuditEventModel, event_id)
            assert event is not None
            assert event.actor_subject == "keycloak-subject-123"
            assert event.action == "activate"
            assert event.target_rule_set_id == "rs-1"
            assert event.outcome == "SUCCEEDED"
            assert event.detail == "Activated after validation"
            assert event.occurred_at == occurred_at
            assert len(SqlAlchemyRuleSetAuditRepository(session).list_for_target("rs-1")) == 1
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        (
            {
                "actor_subject": " ",
                "action": "activate",
                "target_rule_set_id": "rs-1",
                "outcome": "SUCCEEDED",
            },
            "actor subject is required",
        ),
        (
            {
                "actor_subject": "admin-1",
                "action": "unknown",
                "target_rule_set_id": "rs-1",
                "outcome": "SUCCEEDED",
            },
            "Unsupported rule-set audit action",
        ),
        (
            {
                "actor_subject": "admin-1",
                "action": "activate",
                "target_rule_set_id": "rs-1",
                "outcome": "maybe",
            },
            "Unsupported rule-set audit outcome",
        ),
    ],
)
def test_rule_set_audit_rejects_invalid_event_metadata(kwargs, message):
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as session:
            with pytest.raises(ValueError, match=message):
                SqlAlchemyRuleSetAuditRepository(session).record(**kwargs)
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()



def test_failed_lifecycle_attempt_is_written_in_independent_committed_transaction():
    from sqlalchemy.orm import sessionmaker

    from infrastructure.database.models import RuleSetAuditEventModel
    from infrastructure.database.rule_set_audit_writer import (
        record_failed_rule_set_operation,
    )

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    try:
        with factory() as session:
            session.add(
                RuleSetVersionModel(
                    id="rs-fail",
                    version="2026.12",
                    status="DRAFT",
                    created_at=datetime(2026, 10, 21, tzinfo=UTC),
                )
            )
            session.commit()

        event_id = record_failed_rule_set_operation(
            factory,
            actor_subject="keycloak-subject-9",
            action="validate",
            target_rule_set_id="rs-fail",
            detail="Validation rejected: missing evidence mapping",
        )

        with factory() as session:
            event = session.get(RuleSetAuditEventModel, event_id)
            assert event is not None
            assert event.outcome == "FAILED"
            assert event.action == "validate"
            assert event.actor_subject == "keycloak-subject-9"
            assert "missing evidence mapping" in event.detail
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()
