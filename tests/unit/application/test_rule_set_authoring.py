from datetime import date

from packages.application.requirement.rule_set_authoring import RuleSetAuthoringService
from packages.domain.requirement.revisions import RequirementRevision
from packages.domain.requirement.rule_sets import RuleSetStatus


class RuleSets:
    def __init__(self):
        self.items = []
    def add(self, value):
        self.items.append(value)


class Memberships:
    def __init__(self):
        self.items = []
    def add(self, value):
        self.items.append(value)


class Revisions:
    def get(self, key):
        return RequirementRevision(
            key, "req-1", "1", "Requirement", date(2026, 1, 1), None,
            (), (), (), (), ("e1",), True,
        )


def test_authoring_creates_draft_and_membership():
    rule_sets = RuleSets()
    memberships = Memberships()
    result = RuleSetAuthoringService(rule_sets, memberships, Revisions()).create_draft(
        "2026.09.23.2", ("req-1:1",)
    )

    assert result.status == RuleSetStatus.DRAFT
    assert rule_sets.items == [result]
    assert memberships.items[0].requirement_revision == "req-1:1"
