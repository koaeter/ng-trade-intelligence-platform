from datetime import date
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from infrastructure.database.repositories import (
    SqlAlchemyApplicabilityEvaluationRepository,
    SqlAlchemyExportScenarioRepository,
    SqlAlchemyRequirementRepository,
)
from infrastructure.database.session import get_session
from packages.application.scenarios.services import create_scenario, evaluate_scenario, get_scenario
from packages.domain.scenario.models import ExportScenario

app = FastAPI(title="NG Trade Intelligence Platform API", version="0.1.0")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class ExportScenarioRequest(BaseModel):
    product_id: str = Field(min_length=1, max_length=64)
    hs_code: str = Field(min_length=1, max_length=32)
    origin_country_code: str = Field(min_length=2, max_length=2)
    destination_market_code: str = Field(min_length=1, max_length=32)
    scenario_date: date


class ExportScenarioResponse(ExportScenarioRequest):
    id: str


class EvaluationResponse(BaseModel):
    scenario_id: str
    result: str
    rule_set_version: str


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="ng-trade-intelligence-api", version="0.1.0")


@app.post("/api/v1/export-scenarios", response_model=ExportScenarioResponse, status_code=201, tags=["scenarios"])
def create_export_scenario(payload: ExportScenarioRequest, session: Session = Depends(get_session)) -> ExportScenarioResponse:
    scenario = ExportScenario(str(uuid4()), payload.product_id, payload.hs_code, payload.origin_country_code.upper(), payload.destination_market_code, payload.scenario_date)
    create_scenario(SqlAlchemyExportScenarioRepository(session), scenario)
    session.commit()
    return ExportScenarioResponse(**payload.model_dump(), id=scenario.id, origin_country_code=scenario.origin_country_code)


@app.get("/api/v1/export-scenarios/{scenario_id}", response_model=ExportScenarioResponse, tags=["scenarios"])
def get_export_scenario(scenario_id: str, session: Session = Depends(get_session)) -> ExportScenarioResponse:
    scenario = get_scenario(SqlAlchemyExportScenarioRepository(session), scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Export scenario not found")
    return ExportScenarioResponse(id=scenario.id, product_id=scenario.product_id, hs_code=scenario.hs_code, origin_country_code=scenario.origin_country_code, destination_market_code=scenario.destination_market_code, scenario_date=scenario.scenario_date)


@app.post("/api/v1/export-scenarios/{scenario_id}/evaluate", response_model=list[EvaluationResponse], tags=["scenarios"])
def evaluate_export_scenario(scenario_id: str, session: Session = Depends(get_session)) -> list[EvaluationResponse]:
    try:
        evaluations = evaluate_scenario(SqlAlchemyExportScenarioRepository(session), SqlAlchemyRequirementRepository(session), SqlAlchemyApplicabilityEvaluationRepository(session), scenario_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    session.commit()
    return [EvaluationResponse(scenario_id=x.scenario_id, result=x.result.value, rule_set_version=x.rule_set_version) for x in evaluations]


@app.get("/api/v1/export-scenarios/{scenario_id}/results", response_model=list[EvaluationResponse], tags=["scenarios"])
def get_export_scenario_results(scenario_id: str, session: Session = Depends(get_session)) -> list[EvaluationResponse]:
    if get_scenario(SqlAlchemyExportScenarioRepository(session), scenario_id) is None:
        raise HTTPException(status_code=404, detail="Export scenario not found")
    evaluations = SqlAlchemyApplicabilityEvaluationRepository(session).list_for_scenario(scenario_id)
    return [EvaluationResponse(scenario_id=x.scenario_id, result=x.result.value, rule_set_version=x.rule_set_version) for x in evaluations]
