"""Seed a controlled development fixture. This data is fictional and non-authoritative."""
from datetime import date

from infrastructure.database.repositories import (
    SqlAlchemyDocumentRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemyHSCodeRepository,
    SqlAlchemyProductRepository,
    SqlAlchemyProvisionRepository,
    SqlAlchemyRequirementRepository,
    SqlAlchemySourceRepository,
)
from infrastructure.database.session import SessionLocal
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.source.models import Document, Provision, Source, SourceStatus


def seed() -> None:
    with SessionLocal() as session:
        source_repo = SqlAlchemySourceRepository(session)
        document_repo = SqlAlchemyDocumentRepository(session)
        provision_repo = SqlAlchemyProvisionRepository(session)
        evidence_repo = SqlAlchemyEvidenceRepository(session)
        requirement_repo = SqlAlchemyRequirementRepository(session)
        product_repo = SqlAlchemyProductRepository(session)
        hs_repo = SqlAlchemyHSCodeRepository(session)

        source = Source(
            "development-regulatory-fixture",
            "Development Regulatory Fixture",
            "NG Trade Intelligence Platform Development",
            "DEVELOPMENT_FIXTURE",
            "TEST",
            None,
            SourceStatus.REVIEWED,
        )
        document = Document(
            "development-export-guideline",
            source.id,
            "Development Export Guideline",
            "GUIDELINE",
            date(2026, 1, 1),
            date(2026, 1, 1),
            None,
            "fixture-1",
        )
        provision = Provision(
            "DEV-4.2",
            document.id,
            "section-4.2",
            "Development fixture: cocoa exports require a fictional export checklist for testing.",
            "REQUIREMENT",
        )
        evidence = Evidence(
            "evidence-dev-001",
            "PROVISION",
            source.id,
            provision.locator,
            provision.text,
            True,
            document.id,
            provision.id,
        )
        product = product_repo.get("cocoa")
        hs_code = hs_repo.get("HS2022", "1801")
        if product is None or hs_code is None:
            raise RuntimeError("Run seed_master_data.py before the regulatory fixture.")

        requirement = Requirement(
            "dev-export-document-requirement",
            "Development fixture export checklist",
            date(2026, 1, 1),
            products=frozenset({product}),
            hs_codes=frozenset({hs_code}),
            evidence_ids=(evidence.id,),
        )

        if source_repo.get(source.id) is None:
            source_repo.add(source)
        if document_repo.get(document.id) is None:
            document_repo.add(document)
        if provision_repo.get(provision.id) is None:
            provision_repo.add(provision)
        if evidence_repo.get(evidence.id) is None:
            evidence_repo.add(evidence)
        if requirement_repo.get(requirement.id) is None:
            requirement_repo.add(requirement)
        session.commit()


if __name__ == "__main__":
    seed()
