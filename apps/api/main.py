from urllib.parse import urlparse
from datetime import date
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Query
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
    SqlAlchemyAcquisitionEventRepository,
    SqlAlchemyExtractionComparisonRepository,
    SqlAlchemyExtractionDiffRepository,
    SqlAlchemyExtractionDiffEntryRepository,
    SqlAlchemySourceArtifactRepository,
    SqlAlchemyExtractedTextRepository,
    SqlAlchemyExtractionRunRepository,
    SqlAlchemyExtractionSegmentRepository,
    SqlAlchemyDocumentVersionRepository,
    SqlAlchemyDocumentRelationshipRepository,
)
from infrastructure.database.session import get_session
from infrastructure.database.document_provenance import SqlAlchemyDocumentProvenanceSummaryRepository
from infrastructure.database.authority_endpoint_repositories import SqlAlchemyAuthorityEndpointRepository
from infrastructure.acquisition.http import HTTPSourceFetcher
from packages.application.scenarios.services import create_scenario, evaluate_scenario, get_scenario
from packages.application.source.register_source import RegisterSourceFromEndpoint
from packages.application.source.acquisition_history import GetSourceAcquisitionHistory
from packages.application.source.verify_authority_endpoint import VerifyAuthorityEndpoint
from packages.application.source.source_acquisition import SourceAcquisitionPolicy
from packages.application.source.artifact_query import GetSourceArtifact
from packages.application.source.document_version_artifact_query import ListSourceArtifactsForDocumentVersion
from packages.application.source.document_provenance_query import GetDocumentProvenance
from packages.application.source.document_provenance_summary import GetDocumentProvenanceSummary
from packages.application.source.document_query import GetDocument
from packages.application.source.document_version_query import GetDocumentVersion, ListDocumentVersions
from packages.application.source.document_relationship_query import (
    GetDocumentRelationship,
    ListDocumentRelationships,
)
from packages.application.source.extraction_comparison_query import GetExtractionComparison
from packages.application.source.extraction_diff_query import GetExtractionDiff, ListExtractionDiffs
from packages.application.source.extracted_text_query import GetExtractedText
from packages.application.source.extraction_run_query import GetExtractionRun, ListExtractionRunsForArtifact
from packages.application.source.extraction_segment_query import GetExtractionSegment, ListExtractionSegments
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
    verification_status: str
    last_verified_at: str | None
    verification_note: str | None










class DocumentResponse(BaseModel):
    id: str
    source_id: str
    title: str
    document_type: str
    publication_date: date | None
    effective_from: date | None
    effective_to: date | None
    version_label: str | None


class DocumentRelationshipResponse(BaseModel):
    id: str
    relationship_type: str
    from_version_id: str
    to_version_id: str
    verified: bool
    evidence_reference: str | None
    note: str | None


class DocumentVersionResponse(BaseModel):
    id: str
    document_id: str
    version_label: str | None
    publication_date: date | None
    effective_from: date | None
    effective_to: date | None
    revision_reference: str | None


class ExtractedTextResponse(BaseModel):
    artifact_id: str
    text: str
    extractor: str
    extractor_version: str
    extracted_at: str
    ocr_used: bool


class SourceArtifactResponse(BaseModel):
    id: str
    source_id: str
    document_id: str
    kind: str
    storage_key: str
    checksum_sha256: str
    acquired_at: str
    mime_type: str | None
    original_filename: str | None
    processing_state: str
    acquisition_event_id: str | None
    document_version_id: str | None


class ExtractionSegmentResponse(BaseModel):
    id: str
    artifact_id: str
    extraction_id: str | None
    sequence: int
    text: str
    page_number: int | None
    section: str | None
    source_start: int | None
    source_end: int | None
    locator: str | None


class ExtractionRunResponse(BaseModel):
    id: str
    artifact_id: str
    document_version_id: str | None
    input_checksum_sha256: str
    extractor: str
    extractor_version: str
    extracted_at: str
    ocr_used: bool


class ExtractionComparisonResponse(BaseModel):
    id: str
    baseline_extraction_id: str
    candidate_extraction_id: str
    baseline_input_checksum_sha256: str
    candidate_input_checksum_sha256: str
    baseline_output_sha256: str
    candidate_output_sha256: str
    result: str
    compared_at: str


class ExtractionDiffEntryResponse(BaseModel):
    id: str
    diff_id: str
    entry_type: str
    ordinal: int
    baseline_segment_id: str | None
    candidate_segment_id: str | None
    baseline_sequence: int | None
    candidate_sequence: int | None
    baseline_text_sha256: str | None
    candidate_text_sha256: str | None
    baseline_page_number: int | None
    candidate_page_number: int | None
    baseline_section: str | None
    candidate_section: str | None
    baseline_source_start: int | None
    baseline_source_end: int | None
    candidate_source_start: int | None
    candidate_source_end: int | None
    baseline_locator: str | None
    candidate_locator: str | None


class ExtractionDiffResponse(BaseModel):
    id: str
    comparison_id: str
    baseline_extraction_id: str
    candidate_extraction_id: str
    entry_count: int
    unchanged_count: int
    added_count: int
    removed_count: int
    modified_count: int
    created_at: str
    entries: list[ExtractionDiffEntryResponse]
    entries_truncated: bool


class ExtractionDiffSummaryResponse(BaseModel):
    id: str
    comparison_id: str
    baseline_extraction_id: str
    candidate_extraction_id: str
    entry_count: int
    unchanged_count: int
    added_count: int
    removed_count: int
    modified_count: int
    created_at: str

class DocumentProvenanceSummaryResponse(BaseModel):
    document_id: str
    version_count: int
    artifact_count: int
    relationship_count: int
    extraction_run_count: int
    segment_count: int
    comparison_count: int
    diff_count: int
    diff_entry_count: int


class DocumentProvenanceResponse(BaseModel):
    document_id: str
    versions: list[DocumentVersionResponse]
    artifacts_by_version: dict[str, list[SourceArtifactResponse]]
    relationships_by_version: dict[str, list[DocumentRelationshipResponse]]
    extraction_runs_by_artifact: dict[str, list[ExtractionRunResponse]]
    segments_by_extraction: dict[str, list[ExtractionSegmentResponse]]
    comparisons_by_extraction: dict[str, list[ExtractionComparisonResponse]]
    diffs_by_comparison: dict[str, list[ExtractionDiffSummaryResponse]]
    diff_entries_by_diff: dict[str, list[ExtractionDiffEntryResponse]]
    truncated_collections: list[str]




class EvidenceResponse(BaseModel):
    id: str
    evidence_type: str
    source_id: str
    locator: str
    excerpt: str
    verified: bool
    document_id: str | None
    provision_id: str | None










def _document_response(document) -> DocumentResponse:
    return DocumentResponse(
        id=document.id,
        source_id=document.source_id,
        title=document.title,
        document_type=document.document_type,
        publication_date=document.publication_date,
        effective_from=document.effective_from,
        effective_to=document.effective_to,
        version_label=document.version_label,
    )


def _document_relationship_response(relationship) -> DocumentRelationshipResponse:
    return DocumentRelationshipResponse(
        id=relationship.id,
        relationship_type=relationship.relationship_type.value,
        from_version_id=relationship.from_version_id,
        to_version_id=relationship.to_version_id,
        verified=relationship.verified,
        evidence_reference=relationship.evidence_reference,
        note=relationship.note,
    )


def _document_version_response(version) -> DocumentVersionResponse:
    return DocumentVersionResponse(
        id=version.id,
        document_id=version.document_id,
        version_label=version.version_label,
        publication_date=version.publication_date,
        effective_from=version.effective_from,
        effective_to=version.effective_to,
        revision_reference=version.revision_reference,
    )


def _extracted_text_response(extracted) -> ExtractedTextResponse:
    return ExtractedTextResponse(
        artifact_id=extracted.artifact_id,
        text=extracted.text,
        extractor=extracted.extractor,
        extractor_version=extracted.extractor_version,
        extracted_at=extracted.extracted_at.isoformat(),
        ocr_used=extracted.ocr_used,
    )


def _source_artifact_response(artifact) -> SourceArtifactResponse:
    return SourceArtifactResponse(
        id=artifact.id,
        source_id=artifact.source_id,
        document_id=artifact.document_id,
        kind=artifact.kind.value,
        storage_key=artifact.storage_key,
        checksum_sha256=artifact.checksum_sha256,
        acquired_at=artifact.acquired_at.isoformat(),
        mime_type=artifact.mime_type,
        original_filename=artifact.original_filename,
        processing_state=artifact.processing_state.value,
        acquisition_event_id=artifact.acquisition_event_id,
        document_version_id=artifact.document_version_id,
    )


def _extraction_segment_response(segment) -> ExtractionSegmentResponse:
    return ExtractionSegmentResponse(
        id=segment.id,
        artifact_id=segment.artifact_id,
        extraction_id=segment.extraction_id,
        sequence=segment.sequence,
        text=segment.text,
        page_number=segment.page_number,
        section=segment.section,
        source_start=segment.source_start,
        source_end=segment.source_end,
        locator=segment.locator,
    )


def _extraction_run_response(extraction) -> ExtractionRunResponse:
    return ExtractionRunResponse(
        id=extraction.id,
        artifact_id=extraction.artifact_id,
        document_version_id=extraction.document_version_id,
        input_checksum_sha256=extraction.input_checksum_sha256,
        extractor=extraction.extractor,
        extractor_version=extraction.extractor_version,
        extracted_at=extraction.extracted_at.isoformat(),
        ocr_used=extraction.ocr_used,
    )


def _extraction_comparison_response(comparison) -> ExtractionComparisonResponse:
    return ExtractionComparisonResponse(
        id=comparison.id,
        baseline_extraction_id=comparison.baseline_extraction_id,
        candidate_extraction_id=comparison.candidate_extraction_id,
        baseline_input_checksum_sha256=comparison.baseline_input_checksum_sha256,
        candidate_input_checksum_sha256=comparison.candidate_input_checksum_sha256,
        baseline_output_sha256=comparison.baseline_output_sha256,
        candidate_output_sha256=comparison.candidate_output_sha256,
        result=comparison.result.value,
        compared_at=comparison.compared_at.isoformat(),
    )


def _extraction_diff_entry_response(entry) -> ExtractionDiffEntryResponse:
    return ExtractionDiffEntryResponse(
        id=entry.id,
        diff_id=entry.diff_id,
        entry_type=entry.entry_type.value,
        ordinal=entry.ordinal,
        baseline_segment_id=entry.baseline_segment_id,
        candidate_segment_id=entry.candidate_segment_id,
        baseline_sequence=entry.baseline_sequence,
        candidate_sequence=entry.candidate_sequence,
        baseline_text_sha256=entry.baseline_text_sha256,
        candidate_text_sha256=entry.candidate_text_sha256,
        baseline_page_number=entry.baseline_page_number,
        candidate_page_number=entry.candidate_page_number,
        baseline_section=entry.baseline_section,
        candidate_section=entry.candidate_section,
        baseline_source_start=entry.baseline_source_start,
        baseline_source_end=entry.baseline_source_end,
        candidate_source_start=entry.candidate_source_start,
        candidate_source_end=entry.candidate_source_end,
        baseline_locator=entry.baseline_locator,
        candidate_locator=entry.candidate_locator,
    )


def _extraction_diff_summary_response(diff) -> ExtractionDiffSummaryResponse:
    return ExtractionDiffSummaryResponse(
        id=diff.id,
        comparison_id=diff.comparison_id,
        baseline_extraction_id=diff.baseline_extraction_id,
        candidate_extraction_id=diff.candidate_extraction_id,
        entry_count=diff.entry_count,
        unchanged_count=diff.unchanged_count,
        added_count=diff.added_count,
        removed_count=diff.removed_count,
        modified_count=diff.modified_count,
        created_at=diff.created_at.isoformat(),
    )









@app.get("/api/v1/documents/{document_id}/provenance/summary", response_model=DocumentProvenanceSummaryResponse, tags=["sources"])
def get_document_provenance_summary(
    document_id: str,
    session: Session = Depends(get_session),
) -> DocumentProvenanceSummaryResponse:
    try:
        summary = GetDocumentProvenanceSummary(
            SqlAlchemyDocumentProvenanceSummaryRepository(session)
        ).execute(document_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return DocumentProvenanceSummaryResponse(
        document_id=summary.document_id,
        version_count=summary.version_count,
        artifact_count=summary.artifact_count,
        relationship_count=summary.relationship_count,
        extraction_run_count=summary.extraction_run_count,
        segment_count=summary.segment_count,
        comparison_count=summary.comparison_count,
        diff_count=summary.diff_count,
        diff_entry_count=summary.diff_entry_count,
    )


@app.get("/api/v1/documents/{document_id}/provenance", response_model=DocumentProvenanceResponse, tags=["sources"])
def get_document_provenance(
    document_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> DocumentProvenanceResponse:
    if SqlAlchemyDocumentRepository(session).get(document_id) is None:
        raise HTTPException(status_code=404, detail="Document not found")
    view = GetDocumentProvenance(
        SqlAlchemyDocumentVersionRepository(session),
        SqlAlchemySourceArtifactRepository(session),
        SqlAlchemyDocumentRelationshipRepository(session),
        SqlAlchemyExtractionRunRepository(session),
        SqlAlchemyExtractionSegmentRepository(session),
        SqlAlchemyExtractionComparisonRepository(session),
        SqlAlchemyExtractionDiffRepository(session),
        SqlAlchemyExtractionDiffEntryRepository(session),
    ).execute(document_id, limit=limit)
    return DocumentProvenanceResponse(
        document_id=document_id,
        versions=[_document_version_response(version) for version in view.versions],
        artifacts_by_version={
            version_id: [_source_artifact_response(artifact) for artifact in artifacts]
            for version_id, artifacts in view.artifacts_by_version.items()
        },
        relationships_by_version={
            version_id: [
                _document_relationship_response(relationship)
                for relationship in relationships
            ]
            for version_id, relationships in view.relationships_by_version.items()
        },
        extraction_runs_by_artifact={
            artifact_id: [
                _extraction_run_response(extraction)
                for extraction in extractions
            ]
            for artifact_id, extractions in view.extraction_runs_by_artifact.items()
        },
        segments_by_extraction={
            extraction_id: [
                _extraction_segment_response(segment)
                for segment in segments
            ]
            for extraction_id, segments in view.segments_by_extraction.items()
        },
        comparisons_by_extraction={
            extraction_id: [
                _extraction_comparison_response(comparison)
                for comparison in comparisons
            ]
            for extraction_id, comparisons in view.comparisons_by_extraction.items()
        },
        diffs_by_comparison={
            comparison_id: [
                _extraction_diff_summary_response(diff)
                for diff in diffs
            ]
            for comparison_id, diffs in view.diffs_by_comparison.items()
        },
        diff_entries_by_diff={
            diff_id: [
                _extraction_diff_entry_response(entry)
                for entry in entries
            ]
            for diff_id, entries in view.diff_entries_by_diff.items()
        },
        truncated_collections=list(view.truncated_collections),
    )


@app.get("/api/v1/documents/{document_id}", response_model=DocumentResponse, tags=["sources"])
def get_document(document_id: str, session: Session = Depends(get_session)) -> DocumentResponse:
    try:
        document = GetDocument(
            SqlAlchemyDocumentRepository(session)
        ).execute(document_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _document_response(document)


@app.get("/api/v1/document-relationships/{relationship_id}", response_model=DocumentRelationshipResponse, tags=["sources"])
def get_document_relationship(
    relationship_id: str,
    session: Session = Depends(get_session),
) -> DocumentRelationshipResponse:
    try:
        relationship = GetDocumentRelationship(
            SqlAlchemyDocumentRelationshipRepository(session)
        ).execute(relationship_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _document_relationship_response(relationship)


@app.get("/api/v1/document-versions/{version_id}/relationships", response_model=list[DocumentRelationshipResponse], tags=["sources"])
def list_document_relationships(
    version_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[DocumentRelationshipResponse]:
    if SqlAlchemyDocumentVersionRepository(session).get(version_id) is None:
        raise HTTPException(status_code=404, detail="Document version not found")
    relationships = ListDocumentRelationships(
        SqlAlchemyDocumentRelationshipRepository(session)
    ).execute(version_id, limit=limit)
    return [_document_relationship_response(relationship) for relationship in relationships]


@app.get("/api/v1/document-versions/{version_id}", response_model=DocumentVersionResponse, tags=["sources"])
def get_document_version(version_id: str, session: Session = Depends(get_session)) -> DocumentVersionResponse:
    try:
        version = GetDocumentVersion(
            SqlAlchemyDocumentVersionRepository(session)
        ).execute(version_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _document_version_response(version)


@app.get("/api/v1/documents/{document_id}/versions", response_model=list[DocumentVersionResponse], tags=["sources"])
def list_document_versions(
    document_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[DocumentVersionResponse]:
    versions = ListDocumentVersions(
        SqlAlchemyDocumentVersionRepository(session)
    ).execute(document_id, limit=limit)
    return [_document_version_response(version) for version in versions]


@app.get("/api/v1/source-artifacts/{artifact_id}/extracted-text", response_model=ExtractedTextResponse, tags=["extraction"])
def get_extracted_text(artifact_id: str, session: Session = Depends(get_session)) -> ExtractedTextResponse:
    try:
        extracted = GetExtractedText(
            SqlAlchemyExtractedTextRepository(session)
        ).execute(artifact_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _extracted_text_response(extracted)


@app.get("/api/v1/document-versions/{version_id}/artifacts", response_model=list[SourceArtifactResponse], tags=["sources"])
def list_document_version_artifacts(
    version_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[SourceArtifactResponse]:
    if SqlAlchemyDocumentVersionRepository(session).get(version_id) is None:
        raise HTTPException(status_code=404, detail="Document version not found")
    artifacts = ListSourceArtifactsForDocumentVersion(
        SqlAlchemySourceArtifactRepository(session)
    ).execute(version_id, limit=limit)
    return [_source_artifact_response(artifact) for artifact in artifacts]


@app.get("/api/v1/source-artifacts/{artifact_id}", response_model=SourceArtifactResponse, tags=["sources"])
def get_source_artifact(artifact_id: str, session: Session = Depends(get_session)) -> SourceArtifactResponse:
    try:
        artifact = GetSourceArtifact(
            SqlAlchemySourceArtifactRepository(session)
        ).execute(artifact_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _source_artifact_response(artifact)



@app.get("/api/v1/source-artifacts/{artifact_id}/extraction-runs", response_model=list[ExtractionRunResponse], tags=["extraction"])
def list_extraction_runs_for_artifact(
    artifact_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[ExtractionRunResponse]:
    runs = ListExtractionRunsForArtifact(
        SqlAlchemyExtractionRunRepository(session)
    ).execute(artifact_id, limit=limit)
    return [_extraction_run_response(extraction) for extraction in runs]


@app.get("/api/v1/extraction-segments/{segment_id}", response_model=ExtractionSegmentResponse, tags=["extraction"])
def get_extraction_segment(segment_id: str, session: Session = Depends(get_session)) -> ExtractionSegmentResponse:
    try:
        segment = GetExtractionSegment(
            SqlAlchemyExtractionSegmentRepository(session)
        ).execute(segment_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _extraction_segment_response(segment)


@app.get("/api/v1/extraction-runs/{extraction_id}/segments", response_model=list[ExtractionSegmentResponse], tags=["extraction"])
def list_extraction_segments(
    extraction_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[ExtractionSegmentResponse]:
    segments = ListExtractionSegments(
        SqlAlchemyExtractionSegmentRepository(session)
    ).execute(extraction_id, limit=limit)
    return [_extraction_segment_response(segment) for segment in segments]


@app.get("/api/v1/extraction-runs/{extraction_id}", response_model=ExtractionRunResponse, tags=["extraction"])
def get_extraction_run(extraction_id: str, session: Session = Depends(get_session)) -> ExtractionRunResponse:
    try:
        extraction = GetExtractionRun(
            SqlAlchemyExtractionRunRepository(session)
        ).execute(extraction_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _extraction_run_response(extraction)


@app.get("/api/v1/extraction-comparisons/{comparison_id}", response_model=ExtractionComparisonResponse, tags=["extraction"])
def get_extraction_comparison(comparison_id: str, session: Session = Depends(get_session)) -> ExtractionComparisonResponse:
    try:
        comparison = GetExtractionComparison(
            SqlAlchemyExtractionComparisonRepository(session)
        ).execute(comparison_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _extraction_comparison_response(comparison)


@app.get("/api/v1/extraction-diffs/{diff_id}", response_model=ExtractionDiffResponse, tags=["extraction"])
def get_extraction_diff(
    diff_id: str,
    entry_limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> ExtractionDiffResponse:
    try:
        diff, entries, entries_truncated = GetExtractionDiff(
            SqlAlchemyExtractionDiffRepository(session),
            SqlAlchemyExtractionDiffEntryRepository(session),
        ).execute(diff_id, entry_limit=entry_limit)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ExtractionDiffResponse(
        **_extraction_diff_summary_response(diff).model_dump(),
        entries=[_extraction_diff_entry_response(entry) for entry in entries],
        entries_truncated=entries_truncated,
    )


@app.get("/api/v1/extraction-comparisons/{comparison_id}/diffs", response_model=list[ExtractionDiffSummaryResponse], tags=["extraction"])
def list_extraction_diffs(
    comparison_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[ExtractionDiffSummaryResponse]:
    comparison = SqlAlchemyExtractionComparisonRepository(session).get(comparison_id)
    if comparison is None:
        raise HTTPException(status_code=404, detail="Extraction comparison not found")
    diffs = ListExtractionDiffs(SqlAlchemyExtractionDiffRepository(session)).execute(comparison_id, limit=limit)
    return [_extraction_diff_summary_response(diff) for diff in diffs]


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


@app.post("/api/v1/authority-endpoints/{endpoint_id}/verify", response_model=AuthorityEndpointResponse, tags=["sources"])
def verify_authority_endpoint(endpoint_id: str, session: Session = Depends(get_session)) -> AuthorityEndpointResponse:
    endpoints = SqlAlchemyAuthorityEndpointRepository(session)
    endpoint = endpoints.get(endpoint_id)
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Authority endpoint not found")
    host = urlparse(endpoint.url).hostname
    if not host:
        raise HTTPException(status_code=400, detail="Authority endpoint URL has no hostname")
    fetcher = HTTPSourceFetcher(SourceAcquisitionPolicy(allowed_hosts=frozenset({host})))
    try:
        verified = VerifyAuthorityEndpoint(endpoints).execute(endpoint_id, fetcher)
    except ValueError as exc:
        session.commit()
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    session.commit()
    return AuthorityEndpointResponse(
        id=verified.id,
        authority_id=verified.authority_id,
        url=verified.url,
        endpoint_type=verified.endpoint_type,
        access_method=verified.access_method,
        content_format=verified.content_format,
        purpose=verified.purpose,
        active=verified.active,
        verification_status=verified.verification_status.value,
        last_verified_at=verified.last_verified_at.isoformat() if verified.last_verified_at else None,
        verification_note=verified.verification_note,
    )


@app.get("/api/v1/authorities/{authority_id}/endpoints", response_model=list[AuthorityEndpointResponse], tags=["sources"])
def list_authority_endpoints(
    authority_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[AuthorityEndpointResponse]:
    endpoints = SqlAlchemyAuthorityEndpointRepository(session).list_for_authority(authority_id, limit=limit)
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
            verification_status=x.verification_status.value,
            last_verified_at=x.last_verified_at.isoformat() if x.last_verified_at else None,
            verification_note=x.verification_note,
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
def list_source_acquisition_events(
    source_id: str,
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[AcquisitionEventResponse]:
    if SqlAlchemySourceRepository(session).get(source_id) is None:
        raise HTTPException(status_code=404, detail="Source not found")
    events = GetSourceAcquisitionHistory(
        SqlAlchemyAcquisitionEventRepository(session)
    ).execute(source_id, limit=limit)
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
