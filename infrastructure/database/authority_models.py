from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class SourceAuthorityAssignmentModel(Base):
    __tablename__ = "source_authority_assignments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_id: Mapped[str] = mapped_column(String(64), ForeignKey("sources.id"), nullable=False, index=True)
    authority_type: Mapped[str] = mapped_column(String(64), nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    fact_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    precedence: Mapped[int] = mapped_column(Integer, nullable=False)
    legal_weight: Mapped[int] = mapped_column(Integer, nullable=False)
    effective_from: Mapped[date | None] = mapped_column(Date)
    effective_to: Mapped[date | None] = mapped_column(Date)
    verification_status: Mapped[str] = mapped_column(String(32), nullable=False)
    supersedes_assignment_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("source_authority_assignments.id"))

    __table_args__ = (
        UniqueConstraint("source_id", "jurisdiction", "domain", "fact_type", "effective_from", name="uq_source_authority_scope"),
    )


class InstrumentModel(Base):
    __tablename__ = "instruments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    document_id: Mapped[str] = mapped_column(String(64), ForeignKey("documents.id"), nullable=False, unique=True, index=True)
    instrument_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    legal_effect: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ACTIVE")
    parties: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    supersedes_instrument_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("instruments.id"))
