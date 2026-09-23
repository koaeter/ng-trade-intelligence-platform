from datetime import date

import pytest

from packages.application.requirement.publication import (
    RequirementPublicationDecision, RequirementPublicationService,
)
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.requirement.candidates import RequirementCandidate
from packages.domain.requirement.scope_candidates import RequirementScopeCandidate


class CandidateRepo:
    def __init__(self, value):
        self.value = value
        self.status = None

    def get(self, key):
        return self.value

    def set_status(self, key, status):
        self.status = status


class ScopeRepo:
    def __init__(self, value):
        self.value = value

    def get(self, key):
        return self.value


class ListRepo:
    def __init__(self, values=()):
        self.values = list(values)
        self.items = []

    def add(self, value):
        self.items.append(value)


class ReviewRepo:
    def __init__(self):
        self.items = []

    def add(self, *args):
        self.items.append(args)


def build_service():
    candidate = RequirementCandidate(
        "candidate-1", "provision-1", "doc-1", "Certificate", "Certificate required."
    )
    scope = RequirementScopeCandidate("candidate-1", product_ids=("p1",))
    return (
        RequirementPublicationService(
            CandidateRepo(candidate),
            ScopeRepo(scope),
            ListRepo(),
            ListRepo([Product("p1", "Cocoa")]),
            ListRepo(),
            ListRepo(),
            ListRepo(),
            ReviewRepo(),
        ),
        candidate,
    )


def test_publication_requires_explicit_scope_review_and_evidence():
    service, _ = build_service()
    with pytest.raises(ValueError, match="scope review"):
        service.publish(
            RequirementPublicationDecision(
                "candidate-1", "reviewer-1", date(2026, 1, 1), None, ("e1",)
            )
        )


def test_publication_creates_structured_requirement():
    service, _ = build_service()
    result = service.publish(
        RequirementPublicationDecision(
            "candidate-1", "reviewer-1", date(2026, 1, 1), None, ("e1",), scope_reviewed=True
        )
    )
    assert result.name == "Certificate"
    assert result.products == frozenset({Product("p1", "Cocoa")})
    assert result.evidence_ids == ("e1",)
