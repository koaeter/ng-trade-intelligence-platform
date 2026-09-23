from datetime import date

import pytest

from packages.application.requirement.rule_set_validation import RuleSetPublicationValidator
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.requirement.revisions import RequirementRevision
from packages.domain.requirement.rule_set_membership import RuleSetRequirementMembership


class Memberships:
    def list_for_rule_set(self, key):
        return [RuleSetRequirementMembership("rs1", "r1", "r1:1")]


class Revisions:
    def __init__(self, revision):
        self.revision = revision
    def get(self, key):
        return self.revision


class Products:
    def get(self, key):
        return Product("p1", "Product")


class HS:
    def get(self, version, code):
        return HSCode(version, code, "Cocoa")


class Countries:
    def get(self, key):
        return Country(key, "Country")


class Markets:
    def get(self, key):
        return Market(key, "Market", key)


class RuleNodes:
    def list_for_requirement(self, key):
        return []


def validator(revision):
    return RuleSetPublicationValidator(
        Memberships(), Revisions(revision), RuleNodes(),
        Products(), HS(), Countries(), Markets(),
    )


def test_valid_rule_set_passes():
    revision = RequirementRevision(
        "r1:1", "r1", "1", "Requirement", date(2026, 1, 1), None,
        ("p1",), (("HS2022", "1801"),), ("NG",), ("DE",), ("e1",), False,
    )
    validator(revision).validate("rs1")


def test_missing_revision_is_rejected():
    with pytest.raises(ValueError, match="missing requirement revision"):
        validator(None).validate("rs1")
