"""Durable writer for failed lifecycle attempts after the business transaction rolls back."""
from collections.abc import Callable
from sqlalchemy.orm import Session

from infrastructure.database.repositories import SqlAlchemyRuleSetAuditRepository


def record_failed_rule_set_operation(
    session_factory: Callable[[], Session],
    *,
    actor_subject: str,
    action: str,
    target_rule_set_id: str,
    detail: str,
) -> str:
    """Persist a failure event in its own transaction.

    Call only after the operation's original transaction has been rolled back.
    This prevents a failure audit event from being discarded with the failed
    state transition. Errors are propagated; callers must not silently ignore
    inability to persist the audit record.
    """
    with session_factory() as session:
        event_id = SqlAlchemyRuleSetAuditRepository(session).record(
            actor_subject=actor_subject,
            action=action,
            target_rule_set_id=target_rule_set_id,
            outcome="FAILED",
            detail=detail,
        )
        session.commit()
        return event_id
