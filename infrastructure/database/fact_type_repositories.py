from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.database.fact_type_models import FactTypeModel
from packages.domain.source.fact_type import FactType


class SqlAlchemyFactTypeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, fact_type: FactType) -> None:
        self._session.add(FactTypeModel(
            id=fact_type.id, name=fact_type.name, code=fact_type.code,
            description=fact_type.description, active=fact_type.active,
        ))
        self._session.flush()

    def _to_domain(self, row: FactTypeModel) -> FactType:
        return FactType(row.id, row.name, row.code, row.description, row.active)

    def get(self, fact_type_id: str) -> FactType | None:
        row = self._session.get(FactTypeModel, fact_type_id)
        return None if row is None else self._to_domain(row)

    def get_by_code(self, code: str) -> FactType | None:
        row = self._session.scalars(select(FactTypeModel).where(FactTypeModel.code == code)).first()
        return None if row is None else self._to_domain(row)
