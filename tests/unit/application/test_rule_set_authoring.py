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



def test_authoring_rejects_duplicate_revision_ids_before_writing():
    rule_sets = RuleSets()
    memberships = Memberships()

    try:
        RuleSetAuthoringService(rule_sets, memberships, Revisions()).create_draft(
            "2026.09.23.3", ("req-1:1", "req-1:1")
        )
    except ValueError as exc:
        assert "Duplicate requirement revision IDs" in str(exc)
    else:
        raise AssertionError("Expected duplicate revision IDs to be rejected")

    assert rule_sets.items == []
    assert memberships.items == []


def test_authoring_rejects_two_revisions_for_same_requirement_before_writing():
    class MultipleRevisions:
        def get(self, key):
            return RequirementRevision(
                key, "req-1", key.rsplit(":", 1)[-1], "Requirement",
                date(2026, 1, 1), None, (), (), (), (), ("e1",), True,
            )

    rule_sets = RuleSets()
    memberships = Memberships()

    try:
        RuleSetAuthoringService(rule_sets, memberships, MultipleRevisions()).create_draft(
            "2026.09.23.4", ("req-1:1", "req-1:2")
        )
    except ValueError as exc:
        assert "one revision per requirement" in str(exc)
    else:
        raise AssertionError("Expected multiple revisions for one requirement to be rejected")

    assert rule_sets.items == []
    assert memberships.items == []
