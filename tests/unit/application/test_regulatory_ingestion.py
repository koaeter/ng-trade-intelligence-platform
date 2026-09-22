from datetime import date

import pytest

from packages.application.ingestion.services import RegulatoryKnowledgeIngestionService
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.source.models import Document, Provision, Source, SourceStatus


class Store:
    def __init__(self) -> None:
        self.items: list[object] = []

    def add(self, item: object) -> None:
        self.items.append(item)

    def get(self, item_id: str) -> object | None:
        return next((x for x in self.items if getattr(x, "id", None) == item_id), None)


def make_service() -> tuple[RegulatoryKnowledgeIngestionService, Store]:
    stores = [Store() for _ in range(5)]
    service = RegulatoryKnowledgeIngestionService(*stores)  # type: ignore[arg-type]
    return service, stores[4]


def test_publication_requires_reviewed_source_and_verified_evidence() -> None:
    service, requirements = make_service()
    source = Source("src", "Fixture", "Test", "DEVELOPMENT", status=SourceStatus.CANDIDATE)
    document = Document("doc", "src", "Fixture document", "GUIDELINE")
    provision = Provision("prov", "doc", "section-1", "Fixture text", "REQUIREMENT")
    evidence = Evidence("ev", "PROVISION", "src", "section-1", "Fixture text", False, "doc", "prov")
    requirement = Requirement("req", "Fixture requirement", date(2026, 1, 1), evidence_ids=("ev",))

    with pytest.raises(ValueError, match="reviewed"):
        service.publish_requirement(source, document, provision, evidence, requirement)
    assert requirements.items == []


def test_publication_accepts_reviewed_source_with_verified_evidence() -> None:
    service, requirements = make_service()
    source = Source("src", "Fixture", "Test", "DEVELOPMENT", status=SourceStatus.REVIEWED)
    document = Document("doc", "src", "Fixture document", "GUIDELINE")
    provision = Provision("prov", "doc", "section-1", "Fixture text", "REQUIREMENT")
    evidence = Evidence("ev", "PROVISION", "src", "section-1", "Fixture text", True, "doc", "prov")
    requirement = Requirement("req", "Fixture requirement", date(2026, 1, 1), evidence_ids=("ev",))

    result = service.publish_requirement(source, document, provision, evidence, requirement)

    assert result.id == "req"
    assert requirements.items == [requirement]
