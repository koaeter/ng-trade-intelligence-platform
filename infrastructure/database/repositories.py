from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import uuid4

from infrastructure.database.models import (
    ApplicabilityEvaluationModel, CountryModel, DocumentModel, EvidenceModel,
    ExportScenarioModel, ExtractedTextModel, HSCodeModel, MarketModel, ProductModel,
    ProvisionModel, RequirementDestinationMarketModel, RequirementEvidenceModel,
    RequirementHSCodeModel, RequirementModel, RequirementOriginCountryModel,
    RequirementProductModel, SourceArtifactModel, SourceModel, ExtractionRunModel, ExtractionComparisonModel, ExtractionSegmentModel, ProvisionCandidateModel,
    AcquisitionEventModel, DocumentVersionModel, DocumentRelationshipModel, ExtractionDiffModel, ExtractionDiffEntryModel,
)
from packages.application.catalog.repositories import CountryRepository, HSCodeRepository, MarketRepository, ProductRepository
from packages.application.scenarios.repositories import ApplicabilityEvaluationRepository, EvidenceRepository, ExportScenarioRepository, RequirementRepository
from packages.application.source.artifact_repositories import ExtractedTextRepository, SourceArtifactRepository
from packages.application.source.extraction_repositories import (
    ExtractionComparisonRepository, ExtractionRunRepository, ExtractionSegmentRepository,
    ExtractionDiffRepository, ExtractionDiffEntryRepository,
)
from packages.application.source.repositories import DocumentRepository, ProvisionRepository, SourceRepository
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ApplicabilityEvaluation, EvaluationResult, ExportScenario
from packages.domain.source.artifacts import ArtifactKind, ArtifactProcessingState, ExtractedText, SourceArtifact
from packages.domain.source.extraction import ExtractionComparison, ExtractionComparisonResult, ExtractionRun, ExtractionSegment
from packages.domain.source.extraction_diff import ExtractionDiff, ExtractionDiffEntry, ExtractionDiffEntryType
from packages.domain.source.provision_candidates import ProvisionCandidate, ProvisionCandidateStatus

from packages.domain.source.models import Document, Provision, Source, SourceStatus
from packages.domain.source.document_versions import DocumentVersion
from packages.domain.source.document_relationships import DocumentRelationship, DocumentRelationshipType


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
        self._session.add(RequirementModel(id=requirement.id, name=requirement.name, effective_from=requirement.effective_from, effective_to=requirement.effective_to, scope_is_general=requirement.scope_is_general))
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
        return Requirement(row.id, row.name, row.effective_from, row.effective_to, product_values, hs_values, country_values, market_values, tuple(evidence), row.scope_is_general)
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
    def update(self, source: Source) -> None:
        row = self._session.get(SourceModel, source.id)
        if row is None:
            raise ValueError("Source does not exist")
        row.name = source.name
        row.organization = source.organization
        row.source_type = source.source_type
        row.jurisdiction = source.jurisdiction
        row.official_url = source.official_url
        row.endpoint_id = source.endpoint_id
        row.status = source.status.value
        self._session.flush()

    def add(self, source: Source) -> None:
        self._session.add(SourceModel(id=source.id, name=source.name, organization=source.organization, source_type=source.source_type, jurisdiction=source.jurisdiction, official_url=source.official_url, endpoint_id=source.endpoint_id, status=source.status.value))
        self._session.flush()
    def get(self, source_id: str) -> Source | None:
        row = self._session.get(SourceModel, source_id)
        return None if row is None else Source(row.id, row.name, row.organization, row.source_type, row.jurisdiction, row.official_url, SourceStatus(row.status), row.endpoint_id)


class SqlAlchemyDocumentRepository(DocumentRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, document: Document) -> None:
        self._session.add(DocumentModel(id=document.id, source_id=document.source_id, title=document.title, document_type=document.document_type, publication_date=document.publication_date, effective_from=document.effective_from, effective_to=document.effective_to, version_label=document.version_label))
        self._session.flush()
    def get(self, document_id: str) -> Document | None:
        row = self._session.get(DocumentModel, document_id)
        return None if row is None else Document(row.id, row.source_id, row.title, row.document_type, row.publication_date, row.effective_from, row.effective_to, row.version_label)


class SqlAlchemyDocumentRelationshipRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, relationship: DocumentRelationship) -> None:
        self._session.add(DocumentRelationshipModel(
            id=relationship.id,
            relationship_type=relationship.relationship_type.value,
            from_version_id=relationship.from_version_id,
            to_version_id=relationship.to_version_id,
            verified=relationship.verified,
            evidence_reference=relationship.evidence_reference,
            note=relationship.note,
        ))
        self._session.flush()

    def get(self, relationship_id: str) -> DocumentRelationship | None:
        row = self._session.get(DocumentRelationshipModel, relationship_id)
        if row is None:
            return None
        return DocumentRelationship(
            row.id,
            DocumentRelationshipType(row.relationship_type),
            row.from_version_id,
            row.to_version_id,
            row.verified,
            row.evidence_reference,
            row.note,
        )

    def list_for_version(self, version_id: str) -> list[DocumentRelationship]:
        rows = self._session.scalars(
            select(DocumentRelationshipModel)
            .where(
                (DocumentRelationshipModel.from_version_id == version_id)
                | (DocumentRelationshipModel.to_version_id == version_id)
            )
            .order_by(DocumentRelationshipModel.id)
        ).all()
        return [
            DocumentRelationship(
                row.id,
                DocumentRelationshipType(row.relationship_type),
                row.from_version_id,
                row.to_version_id,
                row.verified,
                row.evidence_reference,
                row.note,
            )
            for row in rows
        ]


class SqlAlchemyDocumentVersionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, version: DocumentVersion) -> None:
        self._session.add(DocumentVersionModel(
            id=version.id,
            document_id=version.document_id,
            version_label=version.version_label,
            publication_date=version.publication_date,
            effective_from=version.effective_from,
            effective_to=version.effective_to,
            revision_reference=version.revision_reference,
        ))
        self._session.flush()

    def get(self, version_id: str) -> DocumentVersion | None:
        row = self._session.get(DocumentVersionModel, version_id)
        if row is None:
            return None
        return DocumentVersion(
            row.id, row.document_id, row.version_label,
            row.publication_date, row.effective_from, row.effective_to,
            row.revision_reference,
        )

    def list_for_document(self, document_id: str) -> list[DocumentVersion]:
        rows = self._session.scalars(
            select(DocumentVersionModel)
            .where(DocumentVersionModel.document_id == document_id)
            .order_by(DocumentVersionModel.effective_from, DocumentVersionModel.id)
        ).all()
        return [
            DocumentVersion(
                row.id, row.document_id, row.version_label,
                row.publication_date, row.effective_from, row.effective_to,
                row.revision_reference,
            )
            for row in rows
        ]


class SqlAlchemyProvisionRepository(ProvisionRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, provision: Provision) -> None:
        self._session.add(ProvisionModel(id=provision.id, document_id=provision.document_id, locator=provision.locator, text=provision.text, provision_type=provision.provision_type))
        self._session.flush()
    def get(self, provision_id: str) -> Provision | None:
        row = self._session.get(ProvisionModel, provision_id)
        return None if row is None else Provision(row.id, row.document_id, row.locator, row.text, row.provision_type)


class SqlAlchemyAcquisitionEventRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, event) -> None:
        self._session.add(AcquisitionEventModel(
            id=event.id,
            source_id=event.source_id,
            endpoint_id=event.endpoint_id,
            requested_url=event.requested_url,
            retrieved_url=event.retrieved_url,
            started_at=event.started_at,
            completed_at=event.completed_at,
            status=event.status.value,
            http_status=event.http_status,
            content_type=event.content_type,
            content_length=event.content_length,
            response_sha256=event.response_sha256,
            user_agent=event.user_agent,
            error_code=event.error_code,
            error_message=event.error_message,
            artifact_id=event.artifact_id,
        ))
        self._session.flush()

    def get(self, event_id: str):
        from packages.domain.source.acquisition import AcquisitionEvent, AcquisitionEventStatus
        row = self._session.get(AcquisitionEventModel, event_id)
        if row is None:
            return None
        return AcquisitionEvent(
            row.id, row.source_id, row.endpoint_id, row.requested_url, row.retrieved_url,
            row.started_at, row.completed_at, AcquisitionEventStatus(row.status),
            row.http_status, row.content_type, row.content_length, row.response_sha256,
            row.user_agent, row.error_code, row.error_message, row.artifact_id,
        )

    def link_artifact(self, event_id: str, artifact_id: str) -> None:
        row = self._session.get(AcquisitionEventModel, event_id)
        if row is None:
            raise ValueError("Acquisition event does not exist")
        row.artifact_id = artifact_id
        self._session.flush()

    def list_for_source(self, source_id: str):
        from packages.domain.source.acquisition import AcquisitionEvent, AcquisitionEventStatus
        rows = self._session.scalars(
            select(AcquisitionEventModel)
            .where(AcquisitionEventModel.source_id == source_id)
            .order_by(AcquisitionEventModel.started_at.desc(), AcquisitionEventModel.id.desc())
        ).all()
        return [
            AcquisitionEvent(
                row.id, row.source_id, row.endpoint_id, row.requested_url, row.retrieved_url,
                row.started_at, row.completed_at, AcquisitionEventStatus(row.status),
                row.http_status, row.content_type, row.content_length, row.response_sha256,
                row.user_agent, row.error_code, row.error_message, row.artifact_id,
            )
            for row in rows
        ]


class SqlAlchemySourceArtifactRepository(SourceArtifactRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, artifact: SourceArtifact) -> None:
        self._session.add(SourceArtifactModel(
            id=artifact.id, source_id=artifact.source_id, document_id=artifact.document_id,
            acquisition_event_id=artifact.acquisition_event_id, document_version_id=artifact.document_version_id,
            kind=artifact.kind.value, storage_key=artifact.storage_key,
            checksum_sha256=artifact.checksum_sha256, acquired_at=artifact.acquired_at,
            mime_type=artifact.mime_type, original_filename=artifact.original_filename,
            processing_state=artifact.processing_state.value,
        ))
        self._session.flush()
    def get(self, artifact_id: str) -> SourceArtifact | None:
        row = self._session.get(SourceArtifactModel, artifact_id)
        if row is None: return None
        return SourceArtifact(
            row.id, row.source_id, row.document_id, ArtifactKind(row.kind),
            row.storage_key, row.checksum_sha256, row.acquired_at,
            row.mime_type, row.original_filename, ArtifactProcessingState(row.processing_state),
            row.acquisition_event_id, row.document_version_id,
        )


class SqlAlchemyExtractedTextRepository(ExtractedTextRepository):
    def __init__(self, session: Session) -> None: self._session = session
    def add(self, text: ExtractedText) -> None:
        self._session.add(ExtractedTextModel(
            artifact_id=text.artifact_id, text=text.text, extractor=text.extractor,
            extractor_version=text.extractor_version, extracted_at=text.extracted_at,
            ocr_used=text.ocr_used,
        ))
        self._session.flush()
    def get(self, artifact_id: str) -> ExtractedText | None:
        row = self._session.get(ExtractedTextModel, artifact_id)
        return None if row is None else ExtractedText(
            row.artifact_id, row.text, row.extractor, row.extractor_version,
            row.extracted_at, row.ocr_used,
        )


class SqlAlchemyExtractionComparisonRepository(ExtractionComparisonRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, comparison: ExtractionComparison) -> None:
        if comparison.baseline_extraction_id == comparison.candidate_extraction_id:
            raise ValueError("An extraction comparison cannot reference the same run twice")
        self._session.add(ExtractionComparisonModel(
            id=comparison.id,
            baseline_extraction_id=comparison.baseline_extraction_id,
            candidate_extraction_id=comparison.candidate_extraction_id,
            baseline_input_checksum_sha256=comparison.baseline_input_checksum_sha256,
            candidate_input_checksum_sha256=comparison.candidate_input_checksum_sha256,
            baseline_output_sha256=comparison.baseline_output_sha256,
            candidate_output_sha256=comparison.candidate_output_sha256,
            result=comparison.result.value,
            compared_at=comparison.compared_at,
        ))
        self._session.flush()

    def get(self, comparison_id: str) -> ExtractionComparison | None:
        row = self._session.get(ExtractionComparisonModel, comparison_id)
        return None if row is None else ExtractionComparison(
            row.id, row.baseline_extraction_id, row.candidate_extraction_id,
            row.baseline_input_checksum_sha256, row.candidate_input_checksum_sha256,
            row.baseline_output_sha256, row.candidate_output_sha256,
            ExtractionComparisonResult(row.result), row.compared_at,
        )

    def find(self, baseline_extraction_id: str, candidate_extraction_id: str) -> ExtractionComparison | None:
        row = self._session.scalars(
            select(ExtractionComparisonModel).where(
                ExtractionComparisonModel.baseline_extraction_id == baseline_extraction_id,
                ExtractionComparisonModel.candidate_extraction_id == candidate_extraction_id,
            )
        ).first()
        return None if row is None else ExtractionComparison(
            row.id, row.baseline_extraction_id, row.candidate_extraction_id,
            row.baseline_input_checksum_sha256, row.candidate_input_checksum_sha256,
            row.baseline_output_sha256, row.candidate_output_sha256,
            ExtractionComparisonResult(row.result), row.compared_at,
        )


class SqlAlchemyExtractionRunRepository(ExtractionRunRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, extraction: ExtractionRun) -> None:
        self._session.add(ExtractionRunModel(
            id=extraction.id,
            artifact_id=extraction.artifact_id,
            document_version_id=extraction.document_version_id,
            input_checksum_sha256=extraction.input_checksum_sha256,
            extractor=extraction.extractor,
            extractor_version=extraction.extractor_version,
            extracted_at=extraction.extracted_at,
            ocr_used=extraction.ocr_used,
        ))
        self._session.flush()

    def get(self, extraction_id: str) -> ExtractionRun | None:
        row = self._session.get(ExtractionRunModel, extraction_id)
        if row is None:
            return None
        return ExtractionRun(
            row.id, row.artifact_id, row.document_version_id,
            row.input_checksum_sha256, row.extractor, row.extractor_version,
            row.extracted_at, row.ocr_used,
        )

    def list_for_artifact(self, artifact_id: str) -> list[ExtractionRun]:
        rows = self._session.scalars(
            select(ExtractionRunModel)
            .where(ExtractionRunModel.artifact_id == artifact_id)
            .order_by(ExtractionRunModel.extracted_at, ExtractionRunModel.id)
        ).all()
        return [
            ExtractionRun(
                row.id, row.artifact_id, row.document_version_id,
                row.input_checksum_sha256, row.extractor, row.extractor_version,
                row.extracted_at, row.ocr_used,
            )
            for row in rows
        ]


class SqlAlchemyExtractionSegmentRepository(ExtractionSegmentRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, segment: ExtractionSegment) -> None:
        self._session.add(ExtractionSegmentModel(
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
        ))
        self._session.flush()

    def list_for_artifact(self, artifact_id: str) -> list[ExtractionSegment]:
        rows = self._session.scalars(
            select(ExtractionSegmentModel)
            .where(ExtractionSegmentModel.artifact_id == artifact_id)
            .order_by(ExtractionSegmentModel.sequence)
        ).all()
        return [
            ExtractionSegment(
                row.id, row.artifact_id, row.sequence, row.text,
                row.page_number, row.section, row.source_start, row.source_end, row.locator,
                row.extraction_id,
            )
            for row in rows
        ]


    def list_for_extraction(self, extraction_id: str) -> list[ExtractionSegment]:
        rows = self._session.scalars(
            select(ExtractionSegmentModel)
            .where(ExtractionSegmentModel.extraction_id == extraction_id)
            .order_by(ExtractionSegmentModel.sequence)
        ).all()
        return [
            ExtractionSegment(
                row.id, row.artifact_id, row.sequence, row.text,
                row.page_number, row.section, row.source_start, row.source_end,
                row.locator, row.extraction_id,
            )
            for row in rows
        ]

class SqlAlchemyExtractionDiffRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, diff: ExtractionDiff) -> None:
        self._session.add(ExtractionDiffModel(
            id=diff.id,
            comparison_id=diff.comparison_id,
            baseline_extraction_id=diff.baseline_extraction_id,
            candidate_extraction_id=diff.candidate_extraction_id,
            entry_count=diff.entry_count,
            unchanged_count=diff.unchanged_count,
            added_count=diff.added_count,
            removed_count=diff.removed_count,
            modified_count=diff.modified_count,
            created_at=diff.created_at,
        ))
        self._session.flush()

    def get(self, diff_id: str) -> ExtractionDiff | None:
        row = self._session.get(ExtractionDiffModel, diff_id)
        if row is None:
            return None
        return ExtractionDiff(row.id, row.comparison_id, row.baseline_extraction_id,
            row.candidate_extraction_id, row.entry_count, row.unchanged_count,
            row.added_count, row.removed_count, row.modified_count, row.created_at)

    def list_for_comparison(self, comparison_id: str) -> list[ExtractionDiff]:
        rows = self._session.scalars(
            select(ExtractionDiffModel)
            .where(ExtractionDiffModel.comparison_id == comparison_id)
            .order_by(ExtractionDiffModel.created_at, ExtractionDiffModel.id)
        ).all()
        return [ExtractionDiff(row.id, row.comparison_id, row.baseline_extraction_id,
            row.candidate_extraction_id, row.entry_count, row.unchanged_count,
            row.added_count, row.removed_count, row.modified_count, row.created_at)
            for row in rows]


class SqlAlchemyExtractionDiffEntryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entry: ExtractionDiffEntry) -> None:
        self._session.add(ExtractionDiffEntryModel(
            id=entry.id, diff_id=entry.diff_id, entry_type=entry.entry_type.value,
            ordinal=entry.ordinal, baseline_segment_id=entry.baseline_segment_id,
            candidate_segment_id=entry.candidate_segment_id,
            baseline_sequence=entry.baseline_sequence, candidate_sequence=entry.candidate_sequence,
            baseline_text_sha256=entry.baseline_text_sha256,
            candidate_text_sha256=entry.candidate_text_sha256,
            baseline_page_number=entry.baseline_page_number,
            candidate_page_number=entry.candidate_page_number,
            baseline_section=entry.baseline_section, candidate_section=entry.candidate_section,
            baseline_source_start=entry.baseline_source_start, baseline_source_end=entry.baseline_source_end,
            candidate_source_start=entry.candidate_source_start, candidate_source_end=entry.candidate_source_end,
            baseline_locator=entry.baseline_locator, candidate_locator=entry.candidate_locator,
        ))
        self._session.flush()

    def list_for_diff(self, diff_id: str) -> list[ExtractionDiffEntry]:
        rows = self._session.scalars(
            select(ExtractionDiffEntryModel)
            .where(ExtractionDiffEntryModel.diff_id == diff_id)
            .order_by(ExtractionDiffEntryModel.ordinal, ExtractionDiffEntryModel.id)
        ).all()
        return [ExtractionDiffEntry(
            row.id, row.diff_id, ExtractionDiffEntryType(row.entry_type), row.ordinal,
            row.baseline_segment_id, row.candidate_segment_id, row.baseline_sequence,
            row.candidate_sequence, row.baseline_text_sha256, row.candidate_text_sha256,
            row.baseline_page_number, row.candidate_page_number, row.baseline_section,
            row.candidate_section, row.baseline_source_start, row.baseline_source_end,
            row.candidate_source_start, row.candidate_source_end, row.baseline_locator,
            row.candidate_locator,
        ) for row in rows]


class SqlAlchemyProvisionCandidateRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, candidate: ProvisionCandidate) -> None:
        self._session.add(ProvisionCandidateModel(
            id=candidate.id,
            document_id=candidate.document_id,
            artifact_id=candidate.artifact_id,
            extraction_segment_id=candidate.extraction_segment_id,
            text=candidate.text,
            locator=candidate.locator,
            candidate_type=candidate.candidate_type,
            status=candidate.status.value,
        ))
        self._session.flush()

    def get(self, candidate_id: str) -> ProvisionCandidate | None:
        row = self._session.get(ProvisionCandidateModel, candidate_id)
        return None if row is None else ProvisionCandidate(
            row.id, row.document_id, row.artifact_id, row.extraction_segment_id,
            row.text, row.locator, row.candidate_type, ProvisionCandidateStatus(row.status),
        )

    def list_for_document(self, document_id: str) -> list[ProvisionCandidate]:
        rows = self._session.scalars(
            select(ProvisionCandidateModel)
            .where(ProvisionCandidateModel.document_id == document_id)
            .order_by(ProvisionCandidateModel.id)
        ).all()
        return [
            ProvisionCandidate(
                row.id, row.document_id, row.artifact_id, row.extraction_segment_id,
                row.text, row.locator, row.candidate_type, ProvisionCandidateStatus(row.status),
            )
            for row in rows
        ]

    def set_status(self, candidate_id: str, status: ProvisionCandidateStatus) -> None:
        row = self._session.get(ProvisionCandidateModel, candidate_id)
        if row is None:
            raise ValueError("Provision candidate does not exist")
        row.status = status.value
        self._session.flush()

 
class SqlAlchemyProvisionCandidateReviewRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        candidate_id: str,
        reviewer_reference: str,
        decision: ProvisionCandidateStatus,
        reason: str | None,
        reviewed_at,
    ) -> None:
        self._session.add(ProvisionCandidateReviewModel(
            id=str(uuid4()),
            candidate_id=candidate_id,
            reviewer_reference=reviewer_reference,
            decision=decision.value,
            reason=reason,
            reviewed_at=reviewed_at,
        ))
        self._session.flush()

 
class SqlAlchemyRequirementCandidateRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, candidate) -> None:
        self._session.add(RequirementCandidateModel(
            id=candidate.id,
            provision_id=candidate.provision_id,
            document_id=candidate.document_id,
            proposed_name=candidate.proposed_name,
            text=candidate.text,
            status=candidate.status.value,
        ))
        self._session.flush()

    def get(self, candidate_id: str):
        row = self._session.get(RequirementCandidateModel, candidate_id)
        if row is None:
            return None
        from packages.domain.requirement.candidates import RequirementCandidate, RequirementCandidateStatus
        return RequirementCandidate(
            row.id, row.provision_id, row.document_id, row.proposed_name,
            row.text, RequirementCandidateStatus(row.status),
        )

    def list_for_provision(self, provision_id: str):
        from packages.domain.requirement.candidates import RequirementCandidate, RequirementCandidateStatus
        rows = self._session.scalars(
            select(RequirementCandidateModel)
            .where(RequirementCandidateModel.provision_id == provision_id)
            .order_by(RequirementCandidateModel.id)
        ).all()
        return [
            RequirementCandidate(
                row.id, row.provision_id, row.document_id, row.proposed_name,
                row.text, RequirementCandidateStatus(row.status),
            )
            for row in rows
        ]

 
class SqlAlchemyRequirementScopeCandidateRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, scope) -> None:
        self._session.merge(RequirementScopeCandidateModel(
            candidate_id=scope.candidate_id,
            product_ids=list(scope.product_ids),
            hs_codes=[list(x) for x in scope.hs_codes],
            origin_country_codes=list(scope.origin_country_codes),
            destination_market_codes=list(scope.destination_market_codes),
            effective_from=scope.effective_from,
            effective_to=scope.effective_to,
            conditions=list(scope.conditions),
        ))
        self._session.flush()

    def get(self, candidate_id: str):
        row = self._session.get(RequirementScopeCandidateModel, candidate_id)
        if row is None:
            return None
        from packages.domain.requirement.scope_candidates import RequirementScopeCandidate
        return RequirementScopeCandidate(
            candidate_id=row.candidate_id,
            product_ids=tuple(row.product_ids),
            hs_codes=tuple(tuple(x) for x in row.hs_codes),
            origin_country_codes=tuple(row.origin_country_codes),
            destination_market_codes=tuple(row.destination_market_codes),
            effective_from=row.effective_from,
            effective_to=row.effective_to,
            conditions=tuple(row.conditions),
        )

 
class SqlAlchemyRequirementCandidateReviewRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, candidate_id: str, reviewer_reference: str, scope_reviewed: bool, reviewed_at) -> None:
        self._session.add(RequirementCandidateReviewModel(
            id=str(uuid4()),
            candidate_id=candidate_id,
            reviewer_reference=reviewer_reference,
            scope_reviewed=scope_reviewed,
            reviewed_at=reviewed_at,
        ))
        self._session.flush()

 
class SqlAlchemyRequirementConditionCandidateRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, condition) -> None:
        from hashlib import sha256
        key = f"{condition.candidate_id}:{condition.field.value}:{condition.operator.value}:{condition.value or ''}"
        condition_id = sha256(key.encode()).hexdigest()[:64]
        self._session.merge(RequirementConditionCandidateModel(
            id=condition_id,
            candidate_id=condition.candidate_id,
            field=condition.field.value,
            operator=condition.operator.value,
            value=condition.value,
        ))
        self._session.flush()

    def list_for_candidate(self, candidate_id: str):
        from packages.domain.requirement.conditions import (
            RequirementConditionCandidate, RequirementConditionField, RequirementConditionOperator,
        )
        rows = self._session.scalars(
            select(RequirementConditionCandidateModel)
            .where(RequirementConditionCandidateModel.candidate_id == candidate_id)
            .order_by(RequirementConditionCandidateModel.id)
        ).all()
        return [
            RequirementConditionCandidate(
                row.candidate_id,
                RequirementConditionField(row.field),
                RequirementConditionOperator(row.operator),
                row.value,
            )
            for row in rows
        ]

 
class SqlAlchemyRequirementRuleNodeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, node) -> None:
        from packages.domain.requirement.rule_nodes import RequirementRuleNodeType
        if node.node_type == RequirementRuleNodeType.GROUP:
            field = operator = None
        else:
            field = node.field.value if node.field else None
            operator = node.operator.value if node.operator else None
        self._session.add(RequirementRuleNodeModel(
            id=node.id,
            requirement_id=node.requirement_id,
            requirement_revision_id=node.requirement_revision_id,
            parent_id=node.parent_id,
            sequence=node.sequence,
            node_type=node.node_type.value,
            group_operator=node.group_operator.value if node.group_operator else None,
            field=field,
            operator=operator,
            value=node.value,
        ))
        self._session.flush()

    def list_for_requirement(self, requirement_id: str):
        from packages.domain.requirement.conditions import RequirementConditionField, RequirementConditionOperator
        from packages.domain.requirement.rule_nodes import RequirementRuleNode, RequirementRuleNodeType
        from packages.domain.requirement.rule_tree import ConditionGroupOperator
        rows = self._session.scalars(
            select(RequirementRuleNodeModel)
            .where(RequirementRuleNodeModel.requirement_id == requirement_id)
            .order_by(RequirementRuleNodeModel.parent_id, RequirementRuleNodeModel.sequence)
        ).all()
        if any(row.requirement_revision_id is None for row in rows):
            raise ValueError("Requirement rule node is not bound to a revision")
        return [
            RequirementRuleNode(
                row.id,
                row.requirement_id,
                row.requirement_revision_id,
                row.parent_id,
                row.sequence,
                RequirementRuleNodeType(row.node_type),
                ConditionGroupOperator(row.group_operator) if row.group_operator else None,
                RequirementConditionField(row.field) if row.field else None,
                RequirementConditionOperator(row.operator) if row.operator else None,
                row.value,
            )
            for row in rows
        ]

 
    def list_for_revision(self, requirement_revision_id: str):
        from packages.domain.requirement.conditions import RequirementConditionField, RequirementConditionOperator
        from packages.domain.requirement.rule_nodes import RequirementRuleNode, RequirementRuleNodeType
        from packages.domain.requirement.rule_tree import ConditionGroupOperator
        rows = self._session.scalars(
            select(RequirementRuleNodeModel)
            .where(RequirementRuleNodeModel.requirement_revision_id == requirement_revision_id)
            .order_by(RequirementRuleNodeModel.parent_id, RequirementRuleNodeModel.sequence)
        ).all()
        if any(row.requirement_revision_id is None for row in rows):
            raise ValueError("Requirement rule node is not bound to a revision")
        return [
            RequirementRuleNode(
                row.id, row.requirement_id, row.requirement_revision_id, row.parent_id,
                row.sequence, RequirementRuleNodeType(row.node_type),
                ConditionGroupOperator(row.group_operator) if row.group_operator else None,
                RequirementConditionField(row.field) if row.field else None,
                RequirementConditionOperator(row.operator) if row.operator else None,
                row.value,
            )
            for row in rows
        ]

class SqlAlchemyApplicabilityTraceRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, trace, rule_set_version: str) -> None:
        from packages.domain.requirement.evaluation import TruthValue
        from packages.domain.scenario.models import EvaluationResult
        self._session.add(ApplicabilityEvaluationTraceModel(
            id=str(uuid4()),
            scenario_id=trace.scenario_id,
            requirement_id=trace.requirement_id,
            rule_set_version=rule_set_version,
            scenario_date=trace.scenario_date,
            temporal_result=trace.temporal_result.value,
            scope_result=trace.scope_result.value,
            condition_result=trace.condition_result.value,
            evidence_result=trace.evidence_result.value,
            final_result=trace.final_result.value,
        ))
        self._session.flush()

    def list_for_scenario(self, scenario_id: str):
        from packages.domain.requirement.evaluation import TruthValue
        from packages.domain.scenario.applicability_trace import ApplicabilityTrace
        from packages.domain.scenario.models import EvaluationResult
        rows = self._session.scalars(
            select(ApplicabilityEvaluationTraceModel)
            .where(ApplicabilityEvaluationTraceModel.scenario_id == scenario_id)
            .order_by(ApplicabilityEvaluationTraceModel.id)
        ).all()
        return [
            ApplicabilityTrace(
                row.scenario_id,
                row.requirement_id,
                row.scenario_date,
                TruthValue(row.temporal_result),
                TruthValue(row.scope_result),
                TruthValue(row.condition_result),
                EvaluationResult(row.evidence_result),
                EvaluationResult(row.final_result),
            )
            for row in rows
        ]

 
class SqlAlchemyRuleSetVersionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, version) -> None:
        self._session.add(RuleSetVersionModel(
            id=version.id,
            version=version.version,
            status=version.status.value,
            created_at=version.created_at,
        ))
        self._session.flush()

    def get(self, version_id: str):
        from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion
        row = self._session.get(RuleSetVersionModel, version_id)
        return None if row is None else RuleSetVersion(
            row.id, row.version, RuleSetStatus(row.status), row.created_at
        )

    def get_active(self):
        from packages.domain.requirement.rule_sets import RuleSetStatus, RuleSetVersion
        rows = self._session.scalars(
            select(RuleSetVersionModel)
            .where(RuleSetVersionModel.status == RuleSetStatus.ACTIVE.value)
            .order_by(RuleSetVersionModel.created_at.desc())
        ).all()
        if not rows:
            return None
        row = rows[0]
        return RuleSetVersion(row.id, row.version, RuleSetStatus(row.status), row.created_at)

    def set_status(self, version_id: str, status) -> None:
        row = self._session.get(RuleSetVersionModel, version_id)
        if row is None:
            raise ValueError("Rule-set version does not exist")
        row.status = status.value
        self._session.flush()

 
class SqlAlchemyRuleSetMembershipRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, membership) -> None:
        self._session.add(RuleSetRequirementMembershipModel(
            rule_set_id=membership.rule_set_id,
            requirement_id=membership.requirement_id,
            requirement_revision=membership.requirement_revision,
        ))
        self._session.flush()

    def list_for_rule_set(self, rule_set_id: str):
        from packages.domain.requirement.rule_set_membership import RuleSetRequirementMembership
        rows = self._session.scalars(
            select(RuleSetRequirementMembershipModel)
            .where(RuleSetRequirementMembershipModel.rule_set_id == rule_set_id)
            .order_by(RuleSetRequirementMembershipModel.requirement_id)
        ).all()
        return [
            RuleSetRequirementMembership(
                row.rule_set_id, row.requirement_id, row.requirement_revision
            )
            for row in rows
        ]

 
class SqlAlchemyRequirementRevisionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, revision) -> None:
        self._session.add(RequirementRevisionModel(
            id=revision.id,
            requirement_id=revision.requirement_id,
            revision=revision.revision,
            name=revision.name,
            effective_from=revision.effective_from,
            effective_to=revision.effective_to,
            product_ids=list(revision.product_ids),
            hs_codes=[list(x) for x in revision.hs_codes],
            origin_country_codes=list(revision.origin_country_codes),
            destination_market_codes=list(revision.destination_market_codes),
            evidence_ids=list(revision.evidence_ids),
            scope_is_general=revision.scope_is_general,
        ))
        self._session.flush()

    def get(self, revision_id: str):
        from packages.domain.requirement.revisions import RequirementRevision
        row = self._session.get(RequirementRevisionModel, revision_id)
        if row is None:
            return None
        return RequirementRevision(
            row.id, row.requirement_id, row.revision, row.name,
            row.effective_from, row.effective_to,
            tuple(row.product_ids),
            tuple(tuple(x) for x in row.hs_codes),
            tuple(row.origin_country_codes),
            tuple(row.destination_market_codes),
            tuple(row.evidence_ids),
            row.scope_is_general,
        )

