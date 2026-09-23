from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.database.regulatory_domain_models import RegulatoryDomainModel
from packages.domain.source.regulatory_domain import RegulatoryDomain


class SqlAlchemyRegulatoryDomainRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, domain: RegulatoryDomain) -> None:
        self._session.add(RegulatoryDomainModel(
            id=domain.id, name=domain.name, code=domain.code,
            description=domain.description, parent_id=domain.parent_id,
            active=domain.active,
        ))
        self._session.flush()

    def _to_domain(self, row: RegulatoryDomainModel) -> RegulatoryDomain:
        return RegulatoryDomain(row.id, row.name, row.code, row.description, row.parent_id, row.active)

    def get(self, domain_id: str) -> RegulatoryDomain | None:
        row = self._session.get(RegulatoryDomainModel, domain_id)
        return None if row is None else self._to_domain(row)

    def get_by_code(self, code: str) -> RegulatoryDomain | None:
        row = self._session.scalars(select(RegulatoryDomainModel).where(RegulatoryDomainModel.code == code)).first()
        return None if row is None else self._to_domain(row)

    def list_children(self, parent_id: str) -> list[RegulatoryDomain]:
        rows = self._session.scalars(
            select(RegulatoryDomainModel).where(RegulatoryDomainModel.parent_id == parent_id)
            .order_by(RegulatoryDomainModel.name)
        ).all()
        return [self._to_domain(row) for row in rows]
