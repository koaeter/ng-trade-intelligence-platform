from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.base import Base


class ProductModel(Base):
    __tablename__ = "products"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class HSVersionModel(Base):
    __tablename__ = "hs_versions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)


class HSCodeModel(Base):
    __tablename__ = "hs_codes"
    version_id: Mapped[str] = mapped_column(String(64), ForeignKey("hs_versions.id"), primary_key=True)
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)


class CountryModel(Base):
    __tablename__ = "countries"
    code: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)


class MarketModel(Base):
    __tablename__ = "markets"
    code: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(2), ForeignKey("countries.code"))


class ExportScenarioModel(Base):
    __tablename__ = "export_scenarios"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(64), ForeignKey("products.id"), nullable=False)
    hs_version_id: Mapped[str] = mapped_column(String(64), ForeignKey("hs_versions.id"), nullable=False)
    hs_code: Mapped[str] = mapped_column(String(32), nullable=False)
    origin_country_code: Mapped[str] = mapped_column(String(2), ForeignKey("countries.code"), nullable=False)
    destination_market_code: Mapped[str] = mapped_column(String(64), ForeignKey("markets.code"), nullable=False)
    scenario_date: Mapped[date] = mapped_column(Date, nullable=False)


class RequirementModel(Base):
    __tablename__ = "requirements"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date)


class RequirementProductModel(Base):
    __tablename__ = "requirement_products"
    requirement_id: Mapped[str] = mapped_column(String(64), ForeignKey("requirements.id"), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(64), ForeignKey("products.id"), primary_key=True)


class RequirementHSCodeModel(Base):
    __tablename__ = "requirement_hs_codes"
    requirement_id: Mapped[str] = mapped_column(String(64), ForeignKey("requirements.id"), primary_key=True)
    hs_version_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    hs_code: Mapped[str] = mapped_column(String(32), primary_key=True)


class RequirementOriginCountryModel(Base):
    __tablename__ = "requirement_origin_countries"
    requirement_id: Mapped[str] = mapped_column(String(64), ForeignKey("requirements.id"), primary_key=True)
    country_code: Mapped[str] = mapped_column(String(2), ForeignKey("countries.code"), primary_key=True)


class RequirementDestinationMarketModel(Base):
    __tablename__ = "requirement_destination_markets"
    requirement_id: Mapped[str] = mapped_column(String(64), ForeignKey("requirements.id"), primary_key=True)
    market_code: Mapped[str] = mapped_column(String(64), ForeignKey("markets.code"), primary_key=True)


class RequirementEvidenceModel(Base):
    __tablename__ = "requirement_evidence"
    requirement_id: Mapped[str] = mapped_column(String(64), ForeignKey("requirements.id"), primary_key=True)
    evidence_id: Mapped[str] = mapped_column(String(64), ForeignKey("evidence.id"), primary_key=True)


class SourceModel(Base):
    __tablename__ = "sources"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    organization: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False)
    jurisdiction: Mapped[str | None] = mapped_column(String(128))
    official_url: Mapped[str | None] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="DISCOVERED")


class DocumentModel(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_id: Mapped[str] = mapped_column(String(64), ForeignKey("sources.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    document_type: Mapped[str] = mapped_column(String(64), nullable=False)
    publication_date: Mapped[date | None] = mapped_column(Date)
    effective_from: Mapped[date | None] = mapped_column(Date)
    effective_to: Mapped[date | None] = mapped_column(Date)
    version_label: Mapped[str | None] = mapped_column(String(128))


class ProvisionModel(Base):
    __tablename__ = "provisions"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(64), ForeignKey("documents.id"), nullable=False, index=True)
    locator: Mapped[str] = mapped_column(String(500), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    provision_type: Mapped[str] = mapped_column(String(64), nullable=False)


class EvidenceModel(Base):
    __tablename__ = "evidence"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_id: Mapped[str] = mapped_column(String(64), ForeignKey("sources.id"), nullable=False)
    locator: Mapped[str] = mapped_column(String(500), nullable=False)
    excerpt: Mapped[str] = mapped_column(String(4000), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    document_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("documents.id"))
    provision_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("provisions.id"))


class SourceArtifactModel(Base):
    __tablename__ = "source_artifacts"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_id: Mapped[str] = mapped_column(String(64), ForeignKey("sources.id"), nullable=False, index=True)
    document_id: Mapped[str] = mapped_column(String(64), ForeignKey("documents.id"), nullable=False, index=True)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    acquired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(255))
    original_filename: Mapped[str | None] = mapped_column(String(500))
    processing_state: Mapped[str] = mapped_column(String(32), nullable=False, default="ACQUIRED")


class ExtractedTextModel(Base):
    __tablename__ = "extracted_texts"
    artifact_id: Mapped[str] = mapped_column(String(64), ForeignKey("source_artifacts.id", ondelete="CASCADE"), primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    extractor: Mapped[str] = mapped_column(String(128), nullable=False)
    extractor_version: Mapped[str] = mapped_column(String(64), nullable=False)
    extracted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ocr_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class ApplicabilityEvaluationModel(Base):
    __tablename__ = "applicability_evaluations"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    scenario_id: Mapped[str] = mapped_column(String(64), ForeignKey("export_scenarios.id"), nullable=False, index=True)
    requirement_id: Mapped[str] = mapped_column(String(64), ForeignKey("requirements.id"), nullable=False, index=True)
    result: Mapped[str] = mapped_column(String(32), nullable=False)
    rule_set_version: Mapped[str] = mapped_column(String(64), nullable=False)


class ExtractionSegmentModel(Base):
    __tablename__ = "extraction_segments"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    artifact_id: Mapped[str] = mapped_column(String(64), ForeignKey("source_artifacts.id", ondelete="CASCADE"), nullable=False, index=True)
    sequence: Mapped[int] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    page_number: Mapped[int | None] = mapped_column(nullable=True, index=True)
    section: Mapped[str | None] = mapped_column(String(1000))
    source_start: Mapped[int | None] = mapped_column(nullable=True)
    source_end: Mapped[int | None] = mapped_column(nullable=True)
    locator: Mapped[str | None] = mapped_column(String(1000))


class ProvisionCandidateModel(Base):
    __tablename__ = "provision_candidates"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(64), ForeignKey("documents.id"), nullable=False, index=True)
    artifact_id: Mapped[str] = mapped_column(String(64), ForeignKey("source_artifacts.id", ondelete="CASCADE"), nullable=False, index=True)
    extraction_segment_id: Mapped[str] = mapped_column(String(64), ForeignKey("extraction_segments.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    locator: Mapped[str] = mapped_column(String(1000), nullable=False)
    candidate_type: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

 
class ProvisionCandidateReviewModel(Base):
    __tablename__ = "provision_candidate_reviews"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    candidate_id: Mapped[str] = mapped_column(String(64), ForeignKey("provision_candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer_reference: Mapped[str] = mapped_column(String(255), nullable=False)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

 
class RequirementCandidateModel(Base):
    __tablename__ = "requirement_candidates"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    provision_id: Mapped[str] = mapped_column(String(64), ForeignKey("provisions.id"), nullable=False, index=True, unique=True)
    document_id: Mapped[str] = mapped_column(String(64), ForeignKey("documents.id"), nullable=False, index=True)
    proposed_name: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

 
class RequirementScopeCandidateModel(Base):
    __tablename__ = "requirement_scope_candidates"
    candidate_id: Mapped[str] = mapped_column(String(64), ForeignKey("requirement_candidates.id", ondelete="CASCADE"), primary_key=True)
    product_ids: Mapped[list] = mapped_column(JSON, nullable=False)
    hs_codes: Mapped[list] = mapped_column(JSON, nullable=False)
    origin_country_codes: Mapped[list] = mapped_column(JSON, nullable=False)
    destination_market_codes: Mapped[list] = mapped_column(JSON, nullable=False)
    effective_from: Mapped[date | None] = mapped_column(Date)
    effective_to: Mapped[date | None] = mapped_column(Date)
    conditions: Mapped[list] = mapped_column(JSON, nullable=False)
