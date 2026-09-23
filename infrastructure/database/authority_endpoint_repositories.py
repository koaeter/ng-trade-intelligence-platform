from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.database.authority_endpoint_models import AuthorityEndpointModel
from packages.domain.source.authority_endpoint import AuthorityEndpoint


class SqlAlchemyAuthorityEndpointRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, endpoint: AuthorityEndpoint) -> None:
        self._session.add(AuthorityEndpointModel(
            id=endpoint.id,
            authority_id=endpoint.authority_id,
            url=endpoint.url,
            endpoint_type=endpoint.endpoint_type,
            access_method=endpoint.access_method,
            content_format=endpoint.content_format,
            purpose=endpoint.purpose,
            active=endpoint.active,
        ))
        self._session.flush()

    def _to_domain(self, row: AuthorityEndpointModel) -> AuthorityEndpoint:
        return AuthorityEndpoint(
            row.id, row.authority_id, row.url, row.endpoint_type,
            row.access_method, row.content_format, row.purpose, row.active,
        )

    def get(self, endpoint_id: str) -> AuthorityEndpoint | None:
        row = self._session.get(AuthorityEndpointModel, endpoint_id)
        return None if row is None else self._to_domain(row)

    def list_for_authority(self, authority_id: str) -> list[AuthorityEndpoint]:
        rows = self._session.scalars(
            select(AuthorityEndpointModel)
            .where(
                AuthorityEndpointModel.authority_id == authority_id,
                AuthorityEndpointModel.active.is_(True),
            )
            .order_by(AuthorityEndpointModel.endpoint_type, AuthorityEndpointModel.url)
        ).all()
        return [self._to_domain(row) for row in rows]
