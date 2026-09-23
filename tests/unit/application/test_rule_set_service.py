from datetime import datetime, timezone

from packages.application.requirement.rule_set_service import RuleSetVersionService
from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion


class Repo:
    def __init__(self):
        self.items = {
            "old": RuleSetVersion("old", "2026.1", RuleSetStatus.ACTIVE, datetime.now(timezone.utc)),
            "new": RuleSetVersion("new", "2026.2", RuleSetStatus.RETIRED, datetime.now(timezone.utc)),
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


def test_activation_retires_previous_active_version():
    repo = Repo()
    RuleSetVersionService(repo).activate("new")

    assert repo.items["new"].status == RuleSetStatus.ACTIVE
    assert repo.items["old"].status == RuleSetStatus.RETIRED

 
class Validator:
    def __init__(self):
        self.called = False
    def validate(self, rule_set_id):
        self.called = True


def test_activation_validates_before_status_change():
    repo = Repo()
    validator = Validator()
    RuleSetVersionService(repo, validator).activate("new")
    assert validator.called is True
