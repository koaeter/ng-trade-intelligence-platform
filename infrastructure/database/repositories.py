from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import uuid4

from infrastructure.database.models import (
    ApplicabilityEvaluationModel, CountryModel, DocumentModel, EvidenceModel,
    ExportScenarioModel, HSCodeModel, MarketModel, ProductModel, ProvisionModel,
    RequirementDestinationMarketModel, RequirementEvidenceModel, RequirementHSCodeModel,
    RequirementModel, RequirementOriginCountryModel, RequirementProductModel, SourceModel,
)
from packages.application.catalog.repositories import CountryRepository, HSCodeRepository, MarketRepository, ProductRepository
from packages.application.scenarios.repositories import ApplicabilityEvaluationRepository, EvidenceRepository, ExportScenarioRepository, RequirementRepository
from packages.application.source.repositories import DocumentRepository, ProvisionRepository, SourceRepository
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ApplicabilityEvaluation, EvaluationResult, ExportScenario
from packages.domain.source.models import Document, Provision, Source, SourceStatus


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def get(self, product_id: str) -> Product | None:
        row = self._session.get(ProductModel, product_id)
        return None if row is None else Product(row.id, row.name)


class SqlAlchemyHSCodeRepository(HSCodeRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def get(self, version_id: str, code: str) -> HSCode | None:
        row = self._session.get(HSCodeModel, (version_id, code))
        return None if row is None else HSCode(row.version_id, row.code, row.description)


class SqlAlchemyCountryRepository(CountryRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def get(self, code: str) -> Country | None:
        row = self._session.get(CountryModel, code.upper())
        return None if row is None else Country(row.code, row.name)


class SqlAlchemyMarketRepository(MarketRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def get(self, code: str) -> Market | None:
        row = self._session.get(MarketModel, code)
        return None if row is None else Market(row.code, row.name, row.country_code)


class SqlAlchemyExportScenarioRepository(ExportScenarioRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, scenario: ExportScenario) -> None:
        self._session.add(ExportScenarioModel(
            id=scenario.id, product_id=scenario.product.id, hs_version_id=scenario.hs_code.version_id,
            hs_code=scenario.hs_code.code, origin_country_code=scenario.origin_country.code,
            destination_market_code=scenario.destination_market.code, scenario_date=scenario.scenario_date))
        self._session.flush()
    def get(self, scenario_id: str) -> ExportScenario | None:
        row = self._session.get(ExportScenarioModel, scenario_id)
        if row is None: return None
        product = self._session.get(ProductModel, row.product_id)
        hs = self._session.get(HSCodeModel, (row.hs_version_id, row.hs_code))
        country = self._session.get(CountryModel, row.origin_country_code)
        market = self._session.get(MarketModel, row.destination_market_code)
        if None in (product, hs, country, market): return None
        return ExportScenario(row.id, Product(product.id, product.name), HSCode(hs.version_id, hs.code, hs.description), Country(country.code, country.name), Market(market.code, market.name, market.country_code), row.scenario_date)


class SqlAlchemyRequirementRepository(RequirementRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, requirement: Requirement) -> None:
        self._session.add(RequirementModel(id=requirement.id, name=requirement.name, effective_from=requirement.effective_from, effective_to=requirement.effective_to))
        for x in requirement.products: self._session.add(RequirementProductModel(requirement_id=requirement.id, product_id=x.id))
        for x in requirement.hs_codes: self._session.add(RequirementHSCodeModel(requirement_id=requirement.id, hs_version_id=x.version_id, hs_code=x.code))
        for x in requirement.origin_countries: self._session.add(RequirementOriginCountryModel(requirement_id=requirement.id, country_code=x.code))
        for x in requirement.destination_markets: self._session.add(RequirementDestinationMarketModel(requirement_id=requirement.id, market_code=x.code))
        for x in requirement.evidence_ids: self._session.add(RequirementEvidenceModel(requirement_id=requirement.id, evidence_id=x))
        self._session.flush()
    def _map(self, row: RequirementModel) -> Requirement:
        products = [self._session.get(ProductModel, x.product_id) for x in self._session.scalars(select(RequirementProductModel).where(RequirementProductModel.requirement_id == row.id)).all()]
        hs_rows = self._session.scalars(select(RequirementHSCodeModel).where(RequirementHSCodeModel.requirement_id == row.id)).all()
        countries = [self._session.get(CountryModel, x.country_code) for x in self._session.scalars(select(RequirementOriginCountryModel).where(RequirementOriginCountryModel.requirement_id == row.id)).all()]
        markets = [self._session.get(MarketModel, x.market_code) for x in self._session.scalars(select(RequirementDestinationMarketModel).where(RequirementDestinationMarketModel.requirement_id == row.id)).all()]
        evidence = [x.evidence_id for x in self._session.scalars(select(RequirementEvidenceModel).where(RequirementEvidenceModel.requirement_id == row.id)).all()]
        product_values = frozenset(Product(x.id, x.name) for x in products if x)
        hs_values = frozenset(HSCode(x.version_id, x.code, x.description) for x in (self._session.get(HSCodeModel, (x.hs_version_id, x.hs_code)) for x in hs_rows) if x)
        country_values = frozenset(Country(x.code, x.name) for x in countries if x)
        market_values = frozenset(Market(x.code, x.name, x.country_code) for x in markets if x)
        return Requirement(row.id, row.name, row.effective_from, row.effective_to, product_values, hs_values, country_values, market_values, tuple(evidence))
    def get(self, requirement_id: str) -> Requirement | None:
        row = self._session.get(RequirementModel, requirement_id)
        return None if row is None else self._map(row)
    def list_all(self) -> list[Requirement]:
        return [self._map(row) for row in self._session.scalars(select(RequirementModel).order_by(RequirementModel.id)).all()]


class SqlAlchemyEvidenceRepository(EvidenceRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, evidence: Evidence) -> None:
        self._session.add(EvidenceModel(id=evidence.id, evidence_type=evidence.evidence_type, source_id=evidence.source_id, locator=evidence.locator, excerpt=evidence.excerpt, verified=evidence.verified, document_id=evidence.document_id, provision_id=evidence.provision_id))
        self._session.flush()
    def get(self, evidence_id: str) -> Evidence | None:
        row = self._session.get(EvidenceModel, evidence_id)
        return None if row is None else Evidence(row.id, row.evidence_type, row.source_id, row.locator, row.excerpt, row.verified, row.document_id, row.provision_id)


class SqlAlchemyApplicabilityEvaluationRepository(ApplicabilityEvaluationRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, evaluation: ApplicabilityEvaluation) -> None:
        self._session.add(ApplicabilityEvaluationModel(id=str(uuid4()), scenario_id=evaluation.scenario_id, requirement_id=evaluation.requirement_id, result=evaluation.result.value, rule_set_version=evaluation.rule_set_version))
        self._session.flush()
    def list_for_scenario(self, scenario_id: str) -> list[ApplicabilityEvaluation]:
        rows = self._session.scalars(select(ApplicabilityEvaluationModel).where(ApplicabilityEvaluationModel.scenario_id == scenario_id).order_by(ApplicabilityEvaluationModel.id)).all()
        return [ApplicabilityEvaluation(row.scenario_id, row.requirement_id, EvaluationResult(row.result), row.rule_set_version) for row in rows]


class SqlAlchemySourceRepository(SourceRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, source: Source) -> None:
        self._session.add(SourceModel(id=source.id, name=source.name, organization=source.organization, source_type=source.source_type, jurisdiction=source.jurisdiction, official_url=source.official_url, status=source.status.value))
        self._session.flush()
    def get(self, source_id: str) -> Source | None:
        row = self._session.get(SourceModel, source_id)
        return None if row is None else Source(row.id, row.name, row.organization, row.source_type, row.jurisdiction, row.official_url, SourceStatus(row.status))


class SqlAlchemyDocumentRepository(DocumentRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, document: Document) -> None:
        self._session.add(DocumentModel(id=document.id, source_id=document.source_id, title=document.title, document_type=document.document_type, publication_date=document.publication_date, effective_from=document.effective_from, effective_to=document.effective_to, version_label=document.version_label))
        self._session.flush()
    def get(self, document_id: str) -> Document | None:
        row = self._session.get(DocumentModel, document_id)
        return None if row is None else Document(row.id, row.source_id, row.title, row.document_type, row.publication_date, row.effective_from, row.effective_to, row.version_label)


class SqlAlchemyProvisionRepository(ProvisionRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, provision: Provision) -> None:
        self._session.add(ProvisionModel(id=provision.id, document_id=provision.document_id, locator=provision.locator, text=provision.text, provision_type=provision.provision_type))
        self._session.flush()
    def get(self, provision_id: str) -> Provision | None:
        row = self._session.get(ProvisionModel, provision_id)
        return None if row is None else Provision(row.id, row.document_id, row.locator, row.text, row.provision_type)
