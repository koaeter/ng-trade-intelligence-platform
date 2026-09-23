from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.base import Base


class FactTypeModel(Base):
    __tablename__ = "fact_types"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
