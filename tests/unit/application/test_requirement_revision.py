from datetime import date

from packages.application.requirement.revision_service import RequirementRevisionService
from packages.domain.catalog.models import Product
from packages.domain.requirement.models import Requirement


def test_requirement_revision_is_a_snapshot():
    requirement = Requirement(
        "req-1",
        "Cocoa certificate",
        date(2026, 1, 1),
        products=frozenset({Product("p1", "Cocoa")}),
        evidence_ids=("e1",),
        scope_is_general=False,
    )
    revision = RequirementRevisionService().snapshot(requirement, "r1")

    assert revision.id == "req-1:r1"
    assert revision.requirement_id == "req-1"
    assert revision.revision == "r1"
    assert revision.product_ids == ("p1",)
    assert revision.evidence_ids == ("e1",)
