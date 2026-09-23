from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class AuthorityScopeAssignmentModel(Base):
    __tablename__ = "authority_scope_assignments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    authority_id: Mapped[str] = mapped_column(String(64), ForeignKey("authorities.id", ondelete="CASCADE"), nullable=False, index=True)
    jurisdiction_id: Mapped[str] = mapped_column(String(64), ForeignKey("jurisdictions.id"), nullable=False, index=True)
    regulatory_domain_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    fact_type_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    notes: Mapped[str | None] = mapped_column(Text)
