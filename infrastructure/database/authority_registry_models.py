from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.base import Base


class AuthorityModel(Base):
    __tablename__ = "authorities"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    acronym: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    jurisdiction_id: Mapped[str] = mapped_column(String(64), ForeignKey("jurisdictions.id"), nullable=False, index=True)
    authority_type: Mapped[str] = mapped_column(String(64), nullable=False)
    official_url: Mapped[str | None] = mapped_column(String(1000))
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
