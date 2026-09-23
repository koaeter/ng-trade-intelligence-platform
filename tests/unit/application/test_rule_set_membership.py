import pytest

from packages.application.requirement.rule_set_membership import RuleSetMembershipService


def test_membership_requires_requirement_revision():
    with pytest.raises(ValueError, match="revision"):
        RuleSetMembershipService().add("rule-set-1", "req-1", "")
