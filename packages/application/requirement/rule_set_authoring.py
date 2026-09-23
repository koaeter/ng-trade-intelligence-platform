from datetime import datetime, timezone
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

        resolved = []
        for revision_id in revision_ids:
            revision = self.revisions.get(revision_id)
            if revision is None:
                raise ValueError(f"Requirement revision does not exist: {revision_id}")
            resolved.append(revision)

        rule_set = RuleSetVersion(
            id=str(uuid4()),
            version=version,
            status=RuleSetStatus.DRAFT,
            created_at=datetime.now(timezone.utc),
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
