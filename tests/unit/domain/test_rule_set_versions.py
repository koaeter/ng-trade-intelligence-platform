from datetime import datetime, timezone

from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion


def test_rule_set_version_is_immutable_governance_data():
    version = RuleSetVersion(
        "rule-set-1", "2026.09.23.1", RuleSetStatus.ACTIVE, datetime.now(timezone.utc)
    )
    assert version.version == "2026.09.23.1"
    assert version.status == RuleSetStatus.ACTIVE
