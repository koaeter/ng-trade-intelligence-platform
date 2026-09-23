from datetime import date
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from infrastructure.database.repositories import (
    SqlAlchemyApplicabilityEvaluationRepository,
    SqlAlchemyCountryRepository,
    SqlAlchemyDocumentRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemyExportScenarioRepository,
    SqlAlchemyHSCodeRepository,
    SqlAlchemyMarketRepository,
    SqlAlchemyProductRepository,
    SqlAlchemyProvisionRepository,
    SqlAlchemyRequirementRepository,
    SqlAlchemySourceRepository,
    SqlAlchemyAuthorityEndpointRepository,
    SqlAlchemyAcquisitionEventRepository,
)
from infrastructure.database.session import get_session
from packages.application.scenarios.services import create_scenario, evaluate_scenario, get_scenario
from packages.application.source.register_source import RegisterSourceFromEndpoint
from packages.application.source.acquisition_history import GetSourceAcquisitionHistory
from packages.domain.evidence.models import Evidence
from packages.domain.scenario.models import ExportScenario
from packages.domain.source.models import Document, Provision, Source

app = FastAPI(title="NG Trade Intelligence Platform API", version="0.1.0")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class ExportScenarioRequest(BaseModel):
    product_id: str = Field(min_length=1, max_length=64)
    hs_version_id: str = Field(min_length=1, max_length=64)
    hs_code: str = Field(min_length=1, max_length=32)
    origin_country_code: str = Field(min_length=2, max_length=2)
    destination_market_code: str = Field(min_length=1, max_length=64)
    scenario_date: date


class ExportScenarioResponse(ExportScenarioRequest):
    id: str


class EvaluationResponse(BaseModel):
    scenario_id: str
    requirement_id: str
    result: str
    rule_set_version: str
    evidence_ids: list[str]


class SourceRequest(BaseModel):
    name: str
    organization: str
    source_type: str
    jurisdiction: str | None = None
    endpoint_id: str


class DocumentRequest(BaseModel):
    source_id: str
    title: str
    document_type: str
    publication_date: date | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    version_label: str | None = None


class ProvisionRequest(BaseModel):
    document_id: str
    locator: str
    text: str = Field(min_length=1)
    provision_type: str


class AcquisitionEventResponse(BaseModel):
    id: str
    source_id: str
    endpoint_id: str | None
    requested_url: str
    retrieved_url: str | None
    started_at: str
    completed_at: str
    status: str
    http_status: int | None
    content_type: str | None
    content_length: int | None
    response_sha256: str | None
    user_agent: str | None
    error_code: str | None
    error_message: str | None
    artifact_id: str | None


class AuthorityEndpointResponse(BaseModel):
    id: str
    authority_id: str
    url: str
    endpoint_type: str
    access_method: str
    content_format: str
    purpose: str | None
    active: bool


class EvidenceResponse(BaseModel):
    id: str
    evidence_type: str
    source_id: str
    locator: str
    excerpt: str
    verified: bool
    document_id: str | None
    provision_id: str | None


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="ng-trade-intelligence-api", version="0.1.0")


@app.post("/api/v1/export-scenarios", response_model=ExportScenarioResponse, status_code=201, tags=["scenarios"])
def create_export_scenario(payload: ExportScenarioRequest, session: Session = Depends(get_session)) -> ExportScenarioResponse:
    product = SqlAlchemyProductRepository(session).get(payload.product_id)
    hs_code = SqlAlchemyHSCodeRepository(session).get(payload.hs_version_id, payload.hs_code)
    origin = SqlAlchemyCountryRepository(session).get(payload.origin_country_code)
    market = SqlAlchemyMarketRepository(session).get(payload.destination_market_code)
    if None in (product, hs_code, origin, market):
        raise HTTPException(status_code=400, detail="Unknown product, HS code/version, origin country, or destination market")
    scenario = ExportScenario(str(uuid4()), product, hs_code, origin, market, payload.scenario_date)
    create_scenario(SqlAlchemyExportScenarioRepository(session), scenario)
    session.commit()
    return ExportScenarioResponse(**payload.model_dump(), id=scenario.id, origin_country_code=origin.code)


@app.get("/api/v1/export-scenarios/{scenario_id}", response_model=ExportScenarioResponse, tags=["scenarios"])
def get_export_scenario(scenario_id: str, session: Session = Depends(get_session)) -> ExportScenarioResponse:
    scenario = get_scenario(SqlAlchemyExportScenarioRepository(session), scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Export scenario not found")
    return ExportScenarioResponse(id=scenario.id, product_id=scenario.product.id, hs_version_id=scenario.hs_code.version_id, hs_code=scenario.hs_code.code, origin_country_code=scenario.origin_country.code, destination_market_code=scenario.destination_market.code, scenario_date=scenario.scenario_date)


@app.post("/api/v1/export-scenarios/{scenario_id}/evaluate", response_model=list[EvaluationResponse], tags=["scenarios"])
def evaluate_export_scenario(scenario_id: str, session: Session = Depends(get_session)) -> list[EvaluationResponse]:
    try:
        evaluations = evaluate_scenario(SqlAlchemyExportScenarioRepository(session), SqlAlchemyRequirementRepository(session), SqlAlchemyApplicabilityEvaluationRepository(session), scenario_id, SqlAlchemyEvidenceRepository(session))
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    session.commit()
    return [EvaluationResponse(scenario_id=x.scenario_id, requirement_id=x.requirement_id, result=x.result.value, rule_set_version=x.rule_set_version, evidence_ids=[e.id for e in x.evidence]) for x in evaluations]


@app.get("/api/v1/export-scenarios/{scenario_id}/results", response_model=list[EvaluationResponse], tags=["scenarios"])
def get_export_scenario_results(scenario_id: str, session: Session = Depends(get_session)) -> list[EvaluationResponse]:
    if get_scenario(SqlAlchemyExportScenarioRepository(session), scenario_id) is None:
        raise HTTPException(status_code=404, detail="Export scenario not found")
    evaluations = SqlAlchemyApplicabilityEvaluationRepository(session).list_for_scenario(scenario_id)
    return [EvaluationResponse(scenario_id=x.scenario_id, requirement_id=x.requirement_id, result=x.result.value, rule_set_version=x.rule_set_version, evidence_ids=[e.id for e in x.evidence]) for x in evaluations]


@app.get("/api/v1/authorities/{authority_id}/endpoints", response_model=list[AuthorityEndpointResponse], tags=["sources"])
def list_authority_endpoints(authority_id: str, session: Session = Depends(get_session)) -> list[AuthorityEndpointResponse]:
    endpoints = SqlAlchemyAuthorityEndpointRepository(session).list_for_authority(authority_id)
    return [
        AuthorityEndpointResponse(
            id=x.id,
            authority_id=x.authority_id,
            url=x.url,
            endpoint_type=x.endpoint_type,
            access_method=x.access_method,
            content_format=x.content_format,
            purpose=x.purpose,
            active=x.active,
        )
        for x in endpoints
    ]


@app.post("/api/v1/sources", status_code=201, tags=["sources"])
def create_source(payload: SourceRequest, session: Session = Depends(get_session)):
    source = Source(
        str(uuid4()),
        payload.name,
        payload.organization,
        payload.source_type,
        payload.jurisdiction,
        None,
        endpoint_id=payload.endpoint_id,
    )
    try:
        registered = RegisterSourceFromEndpoint(
            SqlAlchemyAuthorityEndpointRepository(session),
            SqlAlchemySourceRepository(session),
        ).execute(source, payload.endpoint_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    session.commit()
    return registered


@app.get("/api/v1/sources/{source_id}/acquisition-events", response_model=list[AcquisitionEventResponse], tags=["sources"])
def list_source_acquisition_events(source_id: str, session: Session = Depends(get_session)) -> list[AcquisitionEventResponse]:
    if SqlAlchemySourceRepository(session).get(source_id) is None:
        raise HTTPException(status_code=404, detail="Source not found")
    events = GetSourceAcquisitionHistory(
        SqlAlchemyAcquisitionEventRepository(session)
    ).execute(source_id)
    return [
        AcquisitionEventResponse(
            id=x.id,
            source_id=x.source_id,
            endpoint_id=x.endpoint_id,
            requested_url=x.requested_url,
            retrieved_url=x.retrieved_url,
            started_at=x.started_at.isoformat(),
            completed_at=x.completed_at.isoformat(),
            status=x.status.value,
            http_status=x.http_status,
            content_type=x.content_type,
            content_length=x.content_length,
            response_sha256=x.response_sha256,
            user_agent=x.user_agent,
            error_code=x.error_code,
            error_message=x.error_message,
            artifact_id=x.artifact_id,
        )
        for x in events
    ]


@app.get("/api/v1/sources/{source_id}", tags=["sources"])
def get_source(source_id: str, session: Session = Depends(get_session)):
    source = SqlAlchemySourceRepository(session).get(source_id)
    if source is None: raise HTTPException(status_code=404, detail="Source not found")
    return source


@app.post("/api/v1/documents", status_code=201, tags=["sources"])
def create_document(payload: DocumentRequest, session: Session = Depends(get_session)):
    if SqlAlchemySourceRepository(session).get(payload.source_id) is None:
        raise HTTPException(status_code=400, detail="Source not found")
    document = Document(str(uuid4()), **payload.model_dump())
    SqlAlchemyDocumentRepository(session).add(document)
    session.commit()
    return document


@app.get("/api/v1/documents/{document_id}", tags=["sources"])
def get_document(document_id: str, session: Session = Depends(get_session)):
    document = SqlAlchemyDocumentRepository(session).get(document_id)
    if document is None: raise HTTPException(status_code=404, detail="Document not found")
    return document


@app.post("/api/v1/provisions", status_code=201, tags=["sources"])
def create_provision(payload: ProvisionRequest, session: Session = Depends(get_session)):
    if SqlAlchemyDocumentRepository(session).get(payload.document_id) is None:
        raise HTTPException(status_code=400, detail="Document not found")
    provision = Provision(str(uuid4()), **payload.model_dump())
    SqlAlchemyProvisionRepository(session).add(provision)
    session.commit()
    return provision


@app.get("/api/v1/provisions/{provision_id}", tags=["sources"])
def get_provision(provision_id: str, session: Session = Depends(get_session)):
    provision = SqlAlchemyProvisionRepository(session).get(provision_id)
    if provision is None: raise HTTPException(status_code=404, detail="Provision not found")
    return provision


@app.get("/api/v1/evidence/{evidence_id}", response_model=EvidenceResponse, tags=["evidence"])
def get_evidence(evidence_id: str, session: Session = Depends(get_session)) -> EvidenceResponse:
    evidence = SqlAlchemyEvidenceRepository(session).get(evidence_id)
    if evidence is None: raise HTTPException(status_code=404, detail="Evidence not found")
    return EvidenceResponse(id=evidence.id, evidence_type=evidence.evidence_type, source_id=evidence.source_id, locator=evidence.locator, excerpt=evidence.excerpt, verified=evidence.verified, document_id=evidence.document_id, provision_id=evidence.provision_id)
