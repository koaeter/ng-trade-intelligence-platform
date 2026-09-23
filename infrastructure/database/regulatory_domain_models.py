from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class RegulatoryDomainModel(Base):
    __tablename__ = "regulatory_domains"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    parent_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("regulatory_domains.id"))
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
