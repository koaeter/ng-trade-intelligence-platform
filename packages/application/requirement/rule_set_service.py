from typing import Protocol

from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion


class RuleSetVersionRepository(Protocol):
    def get(self, version_id: str) -> RuleSetVersion | None: ...

    def set_status(self, version_id: str, status: RuleSetStatus) -> None: ...

    def activate(self, version_id: str) -> None: ...


class RuleSetValidator(Protocol):
    def validate(self, version_id: str) -> None: ...


class RuleSetAuditRepository(Protocol):
    def record(
        self,
        *,
        actor_subject: str,
        action: str,
        target_rule_set_id: str,
        outcome: str,
    ) -> str: ...


class RuleSetVersionService:
    def __init__(
        self,
        repository: RuleSetVersionRepository,
        validator: RuleSetValidator | None = None,
        *,
        audit_repository: RuleSetAuditRepository | None = None,
        actor_subject: str | None = None,
    ) -> None:
        self.repository = repository
        self.validator = validator
        self.audit_repository = audit_repository
        self.actor_subject = actor_subject

    def _get(self, version_id: str) -> RuleSetVersion:
        target = self.repository.get(version_id)
        if target is None:
            raise ValueError("Rule-set version does not exist")
        return target

    def _require_audit_actor(self) -> None:
        if self.audit_repository is not None and (
            not self.actor_subject or not self.actor_subject.strip()
        ):
            raise ValueError("Actor subject is required when lifecycle auditing is enabled")

    def _record_success(self, action: str, version_id: str) -> None:
        if self.audit_repository is None:
            return
        if not self.actor_subject or not self.actor_subject.strip():
            raise ValueError("Actor subject is required when lifecycle auditing is enabled")
        # Both repositories must share a session/transaction. If recording fails,
        # the caller must roll back the state change rather than commit without audit.
        self.audit_repository.record(
            actor_subject=self.actor_subject,
            action=action,
            target_rule_set_id=version_id,
            outcome="SUCCEEDED",
        )

    def validate(self, version_id: str) -> None:
        target = self._get(version_id)
        if target.status not in {RuleSetStatus.DRAFT, RuleSetStatus.VALIDATED}:
            raise ValueError("Only draft or validated rule sets can be validated")
        self._require_audit_actor()
        self._require_validator()
        assert self.validator is not None
        self.validator.validate(target.id)
        self.repository.set_status(target.id, RuleSetStatus.VALIDATED)
        self._record_success("validate", target.id)

    def publish(self, version_id: str) -> None:
        target = self._get(version_id)
        if target.status != RuleSetStatus.VALIDATED:
            raise ValueError("Only validated rule sets can be published")
        self._require_audit_actor()
        self.repository.set_status(target.id, RuleSetStatus.PUBLISHED)
        self._record_success("publish", target.id)

    def activate(self, version_id: str) -> None:
        target = self._get(version_id)
        if target.status not in {RuleSetStatus.PUBLISHED, RuleSetStatus.ACTIVE}:
            raise ValueError("Only published rule sets can be activated")
        self._require_audit_actor()
        self._require_validator()
        assert self.validator is not None
        # Revalidate immediately before the rule set becomes active.
        self.validator.validate(target.id)
        self.repository.activate(target.id)
        self._record_success("activate", target.id)

    def _require_validator(self) -> None:
        if self.validator is None:
            raise ValueError("Rule-set publication validator is required for this operation")
