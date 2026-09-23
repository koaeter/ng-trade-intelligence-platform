from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.database.jurisdiction_models import JurisdictionModel
from packages.domain.source.jurisdiction import Jurisdiction, JurisdictionType


class SqlAlchemyJurisdictionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, jurisdiction: Jurisdiction) -> None:
        self._session.add(JurisdictionModel(
            id=jurisdiction.id, name=jurisdiction.name,
            jurisdiction_type=jurisdiction.jurisdiction_type.value,
            code=jurisdiction.code, parent_id=jurisdiction.parent_id,
            active=jurisdiction.active,
        ))
        self._session.flush()

    def _to_domain(self, row: JurisdictionModel) -> Jurisdiction:
        return Jurisdiction(
            row.id, row.name, JurisdictionType(row.jurisdiction_type),
            row.code, row.parent_id, row.active,
        )

    def get(self, jurisdiction_id: str) -> Jurisdiction | None:
        row = self._session.get(JurisdictionModel, jurisdiction_id)
        return None if row is None else self._to_domain(row)

    def get_by_code(self, code: str) -> Jurisdiction | None:
        row = self._session.scalars(
            select(JurisdictionModel).where(JurisdictionModel.code == code)
        ).first()
        return None if row is None else self._to_domain(row)

    def list_children(self, parent_id: str) -> list[Jurisdiction]:
        rows = self._session.scalars(
            select(JurisdictionModel).where(JurisdictionModel.parent_id == parent_id)
            .order_by(JurisdictionModel.name)
        ).all()
        return [self._to_domain(row) for row in rows]
