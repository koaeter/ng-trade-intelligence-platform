from datetime import UTC, datetime
from uuid import uuid4

from packages.domain.requirement.rule_set_membership import RuleSetRequirementMembership
from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion


class RuleSetAuthoringService:
    def __init__(self, rule_sets, memberships, revisions) -> None:
        self.rule_sets = rule_sets
        self.memberships = memberships
        self.revisions = revisions

    def create_draft(self, version: str, revision_ids: tuple[str, ...]) -> RuleSetVersion:
        if not version.strip():
            raise ValueError("Rule-set version is required")
        if not revision_ids:
            raise ValueError("A rule set requires at least one requirement revision")
        if len(set(revision_ids)) != len(revision_ids):
            raise ValueError("Duplicate requirement revision IDs are not allowed")

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
        return rule_set
