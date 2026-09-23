from sqlalchemy import select
from sqlalchemy.orm import Session
from infrastructure.database.authority_registry_models import AuthorityModel
from packages.domain.source.authority_registry import Authority


class SqlAlchemyAuthorityRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, authority: Authority) -> None:
        self._session.add(AuthorityModel(
            id=authority.id, name=authority.name, acronym=authority.acronym,
            jurisdiction_id=authority.jurisdiction_id, authority_type=authority.authority_type,
            official_url=authority.official_url, active=authority.active,
        ))
        self._session.flush()

    def _to_domain(self, row: AuthorityModel) -> Authority:
        return Authority(row.id, row.name, row.acronym, row.jurisdiction_id, row.authority_type, row.official_url, row.active)

    def get(self, authority_id: str) -> Authority | None:
        row = self._session.get(AuthorityModel, authority_id)
        return None if row is None else self._to_domain(row)

    def get_by_acronym(self, acronym: str) -> Authority | None:
        row = self._session.scalars(select(AuthorityModel).where(AuthorityModel.acronym == acronym)).first()
        return None if row is None else self._to_domain(row)

    def list_for_jurisdiction(self, jurisdiction_id: str) -> list[Authority]:
        rows = self._session.scalars(
            select(AuthorityModel).where(AuthorityModel.jurisdiction_id == jurisdiction_id)
            .order_by(AuthorityModel.name)
        ).all()
        return [self._to_domain(row) for row in rows]
