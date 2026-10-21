from datetime import UTC, datetime

import pytest

from packages.application.requirement.rule_set_service import RuleSetVersionService
from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion


class Repo:
    def __init__(self):
        self.items = {
            "old": RuleSetVersion("old", "2026.1", RuleSetStatus.ACTIVE, datetime.now(UTC)),
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

    def activate(self, version_id):
        for current_id, current in list(self.items.items()):
            if current.status == RuleSetStatus.ACTIVE and current_id != version_id:
                self.set_status(current_id, RuleSetStatus.RETIRED)
        self.set_status(version_id, RuleSetStatus.ACTIVE)


class Validator:
    def __init__(self):
        self.called = False

    def validate(self, rule_set_id):
        self.called = True


def test_activation_retires_previous_active_version():
    repo = Repo()
    validator = Validator()
    RuleSetVersionService(repo, validator).activate("new")

    assert validator.called is True

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



def test_activation_fails_closed_without_publication_validator():
    with pytest.raises(ValueError, match="validator is required"):
        RuleSetVersionService(Repo()).activate("new")


def test_validation_fails_closed_without_publication_validator():
    with pytest.raises(ValueError, match="validator is required"):
        RuleSetVersionService(Repo()).validate("draft")


def test_publish_requires_validated_status():
    repo = Repo()
    with pytest.raises(ValueError, match="Only validated"):
        RuleSetVersionService(repo).publish("draft")

    repo.set_status("draft", RuleSetStatus.VALIDATED)
    RuleSetVersionService(repo).publish("draft")
    assert repo.items["draft"].status == RuleSetStatus.PUBLISHED


def test_validation_does_not_change_status_if_validator_rejects():
    class RejectingValidator:
        def validate(self, rule_set_id):
            raise ValueError("invalid membership")

    repo = Repo()
    with pytest.raises(ValueError, match="invalid membership"):
        RuleSetVersionService(repo, RejectingValidator()).validate("draft")
    assert repo.items["draft"].status == RuleSetStatus.DRAFT


def test_activation_does_not_retire_current_active_if_validation_fails():
    class RejectingValidator:
        def validate(self, rule_set_id):
            raise ValueError("invalid rule tree")

    repo = Repo()
    with pytest.raises(ValueError, match="invalid rule tree"):
        RuleSetVersionService(repo, RejectingValidator()).activate("new")
    assert repo.items["old"].status == RuleSetStatus.ACTIVE
    assert repo.items["new"].status == RuleSetStatus.PUBLISHED



def test_permission_policy_rejects_missing_identity():
    from packages.application.security.authorization import (
        AuthorizationError,
        require_permission,
    )

    with pytest.raises(AuthorizationError, match="Authentication is required"):
        require_permission(None, "rule_set:activate")


def test_permission_policy_requires_exact_permission():
    from packages.application.security.authorization import (
        AuthenticatedPrincipal,
        AuthorizationError,
        require_permission,
    )

    principal = AuthenticatedPrincipal(
        subject="user-2",
        permissions=frozenset({"rule_set:read"}),
    )
    with pytest.raises(AuthorizationError, match="Missing required permission"):
        require_permission(principal, "rule_set:activate")
