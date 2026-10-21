from datetime import date

import pytest

from packages.application.scenarios.revision_evaluation import RevisionAwareEvaluationService
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.revisions import RequirementRevision
from packages.domain.requirement.rule_set_membership import RuleSetRequirementMembership
from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion
from packages.domain.scenario.models import ExportScenario


def scenario():
    return ExportScenario(
        "s1", Product("p1", "Product"), HSCode("HS2022", "1801", "Cocoa"),
        Country("NG", "Nigeria"), Market("DE", "Germany", "DE"), date(2026, 9, 21),
    )


class Scenarios:
    def get(self, key):
        return scenario()


class RuleSets:
    def get_active(self):
        from datetime import datetime, timezone
        return RuleSetVersion("rs1", "2026.09.23.1", RuleSetStatus.ACTIVE, datetime.now(timezone.utc))


class Memberships:
    def list_for_rule_set(self, key):
        return [RuleSetRequirementMembership("rs1", "r1", "r1:1")]


class Revisions:
    def get(self, key):
        return RequirementRevision(
            "r1:1", "r1", "1", "General", date(2026, 1, 1), None,
            ("p1",), (("HS2022", "1801"),), ("NG",), ("DE",), ("e1",), False,
        )


class Products:
    def get(self, key):
        return Product("p1", "Product")


class HS:
    def get(self, version, code):
        return HSCode(version, code, "Cocoa")


class Countries:
    def get(self, key):
        return Country("NG", "Nigeria")


class Markets:
    def get(self, key):
        return Market("DE", "Germany", "DE")


class Evidence:
    def get(self, key):
        return EvidenceValue


EvidenceValue = EvidenceRecord = EvidenceItem = None


class EvidenceRepo:
    def get(self, key):
        return EvidenceObject()


class EvidenceObject:
    id = "e1"
    evidence_type = "PROVISION"
    source_id = "s1"
    locator = "page=1"
    excerpt = "text"
    verified = True
    document_id = "d1"
    provision_id = "p1"


class RuleNodes:
    def __init__(self):
        self.requested_revisions = []

    def list_for_revision(self, key):
        self.requested_revisions.append(key)
        return []

    def list_for_requirement(self, key):
        raise AssertionError("Revision-aware evaluation must not load nodes by requirement ID")


class Evaluations:
    def add(self, value):
        self.value = value


class Traces:
    def add(self, value, version):
        self.value = value
        self.version = version


def test_revision_aware_service_uses_rule_set_revision():
    rule_nodes = RuleNodes()
    service = RevisionAwareEvaluationService(
        Scenarios(), RuleSets(), Memberships(), Revisions(), rule_nodes,
        Products(), HS(), Countries(), Markets(), EvidenceRepo(), Evaluations(), Traces(),
    )
    result = service.evaluate("s1")
    assert result[0].result.value == "APPLICABLE"
    assert result[0].rule_set_version == "2026.09.23.1"
    assert rule_nodes.requested_revisions == ["r1:1"]



def test_revision_aware_service_rejects_mismatched_membership():
    class MismatchedMemberships:
        def list_for_rule_set(self, key):
            return [RuleSetRequirementMembership("rs1", "r2", "r1:1")]

    service = RevisionAwareEvaluationService(
        Scenarios(), RuleSets(), MismatchedMemberships(), Revisions(), RuleNodes(),
        Products(), HS(), Countries(), Markets(), EvidenceRepo(), Evaluations(), Traces(),
    )

    with pytest.raises(ValueError, match="membership and requirement revision disagree"):
        service.evaluate("s1")
