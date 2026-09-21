from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.base import Base

evaluation_evidence = Table(
    "evaluation_evidence", Base.metadata,
    Column("evaluation_id", String(64), ForeignKey("applicability_evaluations.id"), primary_key=True),
    Column("evidence_id", String(64), ForeignKey("evidence.id"), primary_key=True),
)

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
    hs_version_id: Mapped[str] = mapped_column(String(64), nullable=False)
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

class EvidenceModel(Base):
    __tablename__ = "evidence"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_id: Mapped[str] = mapped_column(String(64), nullable=False)
    locator: Mapped[str] = mapped_column(String(500), nullable=False)
    excerpt: Mapped[str] = mapped_column(String(4000), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class ApplicabilityEvaluationModel(Base):
    __tablename__ = "applicability_evaluations"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    scenario_id: Mapped[str] = mapped_column(String(64), ForeignKey("export_scenarios.id"), nullable=False, index=True)
    requirement_id: Mapped[str] = mapped_column(String(64), ForeignKey("requirements.id"), nullable=False, index=True)
    result: Mapped[str] = mapped_column(String(32), nullable=False)
    rule_set_version: Mapped[str] = mapped_column(String(64), nullable=False)
