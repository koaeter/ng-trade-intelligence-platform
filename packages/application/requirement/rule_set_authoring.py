from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from packages.domain.requirement.revisions import RequirementRevision
from packages.domain.requirement.rule_set_membership import RuleSetRequirementMembership
from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion


class RuleSetRepository(Protocol):
    def add(self, version: RuleSetVersion) -> None: ...


class RuleSetMembershipRepository(Protocol):
    def add(self, membership: RuleSetRequirementMembership) -> None: ...


class RequirementRevisionRepository(Protocol):
    def get(self, revision_id: str) -> RequirementRevision | None: ...


class RuleSetAuditRepository(Protocol):
    def record(
        self,
        *,
        actor_subject: str,
        action: str,
        target_rule_set_id: str | None,
        outcome: str,
    ) -> str: ...


class RuleSetAuthoringService:
    def __init__(
        self,
        rule_sets: RuleSetRepository,
        memberships: RuleSetMembershipRepository,
        revisions: RequirementRevisionRepository,
        *,
        audit_repository: RuleSetAuditRepository | None = None,
        actor_subject: str | None = None,
    ) -> None:
        self.rule_sets = rule_sets
        self.memberships = memberships
        self.revisions = revisions
        self.audit_repository = audit_repository
        self.actor_subject = actor_subject

    def create_draft(self, version: str, revision_ids: tuple[str, ...]) -> RuleSetVersion:
        if not version.strip():
            raise ValueError("Rule-set version is required")
        if not revision_ids:
            raise ValueError("A rule set requires at least one requirement revision")
        if len(set(revision_ids)) != len(revision_ids):
            raise ValueError("Duplicate requirement revision IDs are not allowed")
        if self.audit_repository is not None and (
            not self.actor_subject or not self.actor_subject.strip()
        ):
            raise ValueError("Actor subject is required when lifecycle auditing is enabled")

        resolved = []
        for revision_id in revision_ids:
            revision = self.revisions.get(revision_id)
            if revision is None:
                raise ValueError(f"Requirement revision does not exist: {revision_id}")
            resolved.append(revision)

        requirement_ids = [revision.requirement_id for revision in resolved]
        if len(set(requirement_ids)) != len(requirement_ids):
            raise ValueError("A rule set can include only one revision per requirement")

        rule_set = RuleSetVersion(
            id=str(uuid4()),
            version=version,
            status=RuleSetStatus.DRAFT,
            created_at=datetime.now(UTC),
        )
        self.rule_sets.add(rule_set)
        for revision in resolved:
            self.memberships.add(
                RuleSetRequirementMembership(
                    rule_set.id,
                    revision.requirement_id,
                    revision.id,
                )
            )
        if self.audit_repository is not None:
            assert self.actor_subject is not None
            self.audit_repository.record(
                actor_subject=self.actor_subject,
                action="draft.create",
                target_rule_set_id=rule_set.id,
                outcome="SUCCEEDED",
            )
        return rule_set
