from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class JurisdictionModel(Base):
    __tablename__ = "jurisdictions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    jurisdiction_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    code: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    parent_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("jurisdictions.id"))
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
