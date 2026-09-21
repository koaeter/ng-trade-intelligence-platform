from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import uuid4

from infrastructure.database.models import ApplicabilityEvaluationModel, EvidenceModel, ExportScenarioModel, RequirementModel
from packages.application.scenarios.repositories import (
    ApplicabilityEvaluationRepository,
    EvidenceRepository,
    ExportScenarioRepository,
    RequirementRepository,
)
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ApplicabilityEvaluation, EvaluationResult, ExportScenario


def _split(value: str) -> frozenset[str]:
    return frozenset(item for item in value.split(",") if item)


def _join(values: frozenset[str] | tuple[str, ...]) -> str:
    return ",".join(sorted(values))




class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, product_id: str) -> Product | None:
        row = self._session.get(ProductModel, product_id)
        return None if row is None else Product(row.id, row.name)


class SqlAlchemyHSCodeRepository(HSCodeRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, version_id: str, code: str) -> HSCode | None:
        row = self._session.get(HSCodeModel, (version_id, code))
        return None if row is None else HSCode(row.version_id, row.code, row.description)


class SqlAlchemyCountryRepository(CountryRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, code: str) -> Country | None:
        row = self._session.get(CountryModel, code.upper())
        return None if row is None else Country(row.code, row.name)


class SqlAlchemyMarketRepository(MarketRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, code: str) -> Market | None:
        row = self._session.get(MarketModel, code)
        return None if row is None else Market(row.code, row.name, row.country_code)


class SqlAlchemyExportScenarioRepository(ExportScenarioRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, scenario: ExportScenario) -> None:
        self._session.add(ExportScenarioModel(id=scenario.id, product_id=scenario.product_id, hs_code=scenario.hs_code, origin_country_code=scenario.origin_country_code, destination_market_code=scenario.destination_market_code, scenario_date=scenario.scenario_date))
        self._session.flush()

    def get(self, scenario_id: str) -> ExportScenario | None:
        model = self._session.get(ExportScenarioModel, scenario_id)
        if model is None:
            return None
        return ExportScenario(model.id, model.product_id, model.hs_code, model.origin_country_code, model.destination_market_code, model.scenario_date)


class SqlAlchemyRequirementRepository(RequirementRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, requirement: Requirement) -> None:
        self._session.add(RequirementModel(
            id=requirement.id, name=requirement.name,
            effective_from=requirement.effective_from, effective_to=requirement.effective_to,
            product_ids=_join(requirement.product_ids), hs_codes=_join(requirement.hs_codes),
            origin_country_codes=_join(requirement.origin_country_codes),
            destination_market_codes=_join(requirement.destination_market_codes),
            evidence_ids=_join(requirement.evidence_ids),
        ))
        self._session.flush()

    def get(self, requirement_id: str) -> Requirement | None:
        model = self._session.get(RequirementModel, requirement_id)
        if model is None:
            return None
        return Requirement(model.id, model.name, model.effective_from, model.effective_to, _split(model.product_ids), _split(model.hs_codes), _split(model.origin_country_codes), _split(model.destination_market_codes), tuple(_split(model.evidence_ids)))

    def list_all(self) -> list[Requirement]:
        rows = self._session.scalars(select(RequirementModel).order_by(RequirementModel.id)).all()
        return [Requirement(row.id, row.name, row.effective_from, row.effective_to, _split(row.product_ids), _split(row.hs_codes), _split(row.origin_country_codes), _split(row.destination_market_codes), tuple(_split(row.evidence_ids))) for row in rows]


class SqlAlchemyEvidenceRepository(EvidenceRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, evidence: Evidence) -> None:
        self._session.add(EvidenceModel(id=evidence.id, evidence_type=evidence.evidence_type, source_id=evidence.source_id, locator=evidence.locator, excerpt=evidence.excerpt, verified=evidence.verified))
        self._session.flush()

    def get(self, evidence_id: str) -> Evidence | None:
        model = self._session.get(EvidenceModel, evidence_id)
        return None if model is None else Evidence(model.id, model.evidence_type, model.source_id, model.locator, model.excerpt, model.verified)


class SqlAlchemyApplicabilityEvaluationRepository(ApplicabilityEvaluationRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, evaluation: ApplicabilityEvaluation) -> None:
        evaluation_id = str(uuid4())
        self._session.add(ApplicabilityEvaluationModel(id=evaluation_id, scenario_id=evaluation.scenario_id, requirement_id=evaluation.requirement_id, result=evaluation.result.value, rule_set_version=evaluation.rule_set_version))
        self._session.flush()

    def list_for_scenario(self, scenario_id: str) -> list[ApplicabilityEvaluation]:
        rows = self._session.scalars(select(ApplicabilityEvaluationModel).where(ApplicabilityEvaluationModel.scenario_id == scenario_id).order_by(ApplicabilityEvaluationModel.id)).all()
        return [ApplicabilityEvaluation(row.scenario_id, row.requirement_id, EvaluationResult(row.result), row.rule_set_version) for row in rows]
