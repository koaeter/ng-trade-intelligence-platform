from datetime import datetime, timezone

import pytest

from packages.application.requirement.rule_set_service import RuleSetVersionService
from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion


class Repo:
    def __init__(self):
        self.items = {
            "old": RuleSetVersion("old", "2026.1", RuleSetStatus.ACTIVE, datetime.now(timezone.utc)),
            "new": RuleSetVersion("new", "2026.2", RuleSetStatus.PUBLISHED, datetime.now(timezone.utc)),
            "draft": RuleSetVersion("draft", "2026.3", RuleSetStatus.DRAFT, datetime.now(timezone.utc)),
        }

    def get(self, version_id):
        return self.items.get(version_id)

    def get_active(self):
        return next((x for x in self.items.values() if x.status == RuleSetStatus.ACTIVE), None)

    def set_status(self, version_id, status):
        current = self.items[version_id]
        self.items[version_id] = RuleSetVersion(
            current.id, current.version, status, current.created_at
        )


class Validator:
    def __init__(self):
        self.called = False

    def validate(self, rule_set_id):
        self.called = True


def test_activation_retires_previous_active_version():
    repo = Repo()
    RuleSetVersionService(repo).activate("new")

    assert repo.items["new"].status == RuleSetStatus.ACTIVE
    assert repo.items["old"].status == RuleSetStatus.RETIRED


def test_validation_requires_validator_and_moves_draft_to_validated():
    repo = Repo()
    validator = Validator()
    RuleSetVersionService(repo, validator).validate("draft")

    assert validator.called is True
    assert repo.items["draft"].status == RuleSetStatus.VALIDATED


def test_draft_cannot_be_activated():
    with pytest.raises(ValueError, match="published"):
        RuleSetVersionService(Repo()).activate("draft")
