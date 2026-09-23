from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.database.authority_scope_models import AuthorityScopeAssignmentModel
from packages.domain.source.authority_scope import AuthorityScopeAssignment


class SqlAlchemyAuthorityScopeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, assignment: AuthorityScopeAssignment) -> None:
        self._session.add(AuthorityScopeAssignmentModel(
            id=assignment.id,
            authority_id=assignment.authority_id,
            jurisdiction_id=assignment.jurisdiction_id,
            regulatory_domain_code=assignment.regulatory_domain_code,
            fact_type_code=assignment.fact_type_code,
            active=assignment.active,
            notes=assignment.notes,
        ))
        self._session.flush()

    def _to_domain(self, row: AuthorityScopeAssignmentModel) -> AuthorityScopeAssignment:
        return AuthorityScopeAssignment(
            row.id, row.authority_id, row.jurisdiction_id,
            row.regulatory_domain_code, row.fact_type_code, row.active, row.notes,
        )

    def get(self, assignment_id: str) -> AuthorityScopeAssignment | None:
        row = self._session.get(AuthorityScopeAssignmentModel, assignment_id)
        return None if row is None else self._to_domain(row)

    def list_for_authority(self, authority_id: str) -> list[AuthorityScopeAssignment]:
        rows = self._session.scalars(
            select(AuthorityScopeAssignmentModel)
            .where(AuthorityScopeAssignmentModel.authority_id == authority_id)
            .order_by(AuthorityScopeAssignmentModel.regulatory_domain_code, AuthorityScopeAssignmentModel.fact_type_code)
        ).all()
        return [self._to_domain(row) for row in rows]

    def list_for_scope(self, jurisdiction_id: str, regulatory_domain_code: str, fact_type_code: str) -> list[AuthorityScopeAssignment]:
        rows = self._session.scalars(
            select(AuthorityScopeAssignmentModel)
            .where(
                AuthorityScopeAssignmentModel.jurisdiction_id == jurisdiction_id,
                AuthorityScopeAssignmentModel.regulatory_domain_code == regulatory_domain_code,
                AuthorityScopeAssignmentModel.fact_type_code == fact_type_code,
                AuthorityScopeAssignmentModel.active.is_(True),
            )
            .order_by(AuthorityScopeAssignmentModel.authority_id)
        ).all()
        return [self._to_domain(row) for row in rows]
