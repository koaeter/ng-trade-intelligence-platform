from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.base import Base


class ExportScenarioModel(Base):
    __tablename__ = "export_scenarios"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(64), nullable=False)
    hs_code: Mapped[str] = mapped_column(String(32), nullable=False)
    origin_country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    destination_market_code: Mapped[str] = mapped_column(String(32), nullable=False)
    scenario_date: Mapped[date] = mapped_column(Date, nullable=False)


class RequirementModel(Base):
    __tablename__ = "requirements"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[date | None] = mapped_column(Date, nullable=True)


class ApplicabilityEvaluationModel(Base):
    __tablename__ = "applicability_evaluations"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    scenario_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    result: Mapped[str] = mapped_column(String(32), nullable=False)
    rule_set_version: Mapped[str] = mapped_column(String(64), nullable=False)
