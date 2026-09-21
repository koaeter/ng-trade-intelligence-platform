from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.database.models import ApplicabilityEvaluationModel, ExportScenarioModel, RequirementModel
from packages.application.scenarios.repositories import (
    ApplicabilityEvaluationRepository,
    ExportScenarioRepository,
    RequirementRepository,
)
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ApplicabilityEvaluation, EvaluationResult, ExportScenario


class SqlAlchemyExportScenarioRepository(ExportScenarioRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, scenario: ExportScenario) -> None:
        self._session.add(ExportScenarioModel(
            id=scenario.id, product_id=scenario.product_id, hs_code=scenario.hs_code,
            origin_country_code=scenario.origin_country_code,
            destination_market_code=scenario.destination_market_code,
            scenario_date=scenario.scenario_date,
        ))
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
        self._session.add(RequirementModel(id=requirement.id, name=requirement.name, effective_from=requirement.effective_from, effective_to=requirement.effective_to))
        self._session.flush()

    def get(self, requirement_id: str) -> Requirement | None:
        model = self._session.get(RequirementModel, requirement_id)
        return None if model is None else Requirement(model.id, model.name, model.effective_from, model.effective_to)

    def list_all(self) -> list[Requirement]:
        rows = self._session.scalars(select(RequirementModel).order_by(RequirementModel.id)).all()
        return [Requirement(row.id, row.name, row.effective_from, row.effective_to) for row in rows]


class SqlAlchemyApplicabilityEvaluationRepository(ApplicabilityEvaluationRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, evaluation: ApplicabilityEvaluation) -> None:
        from uuid import uuid4
        self._session.add(ApplicabilityEvaluationModel(id=str(uuid4()), scenario_id=evaluation.scenario_id, result=evaluation.result.value, rule_set_version=evaluation.rule_set_version))
        self._session.flush()

    def list_for_scenario(self, scenario_id: str) -> list[ApplicabilityEvaluation]:
        rows = self._session.scalars(select(ApplicabilityEvaluationModel).where(ApplicabilityEvaluationModel.scenario_id == scenario_id).order_by(ApplicabilityEvaluationModel.id)).all()
        return [ApplicabilityEvaluation(row.scenario_id, EvaluationResult(row.result), row.rule_set_version) for row in rows]
