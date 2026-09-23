from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.database.authority_models import InstrumentModel, SourceAuthorityAssignmentModel
from packages.domain.source.authority import AuthorityType, Instrument, InstrumentStatus, InstrumentType, LegalEffect, SourceAuthorityAssignment


class SqlAlchemySourceAuthorityRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, assignment: SourceAuthorityAssignment) -> None:
        self._session.add(SourceAuthorityAssignmentModel(
            id=assignment.id, source_id=assignment.source_id,
            authority_type=assignment.authority_type.value,
            jurisdiction=assignment.jurisdiction, domain=assignment.domain,
            fact_type=assignment.fact_type, precedence=assignment.precedence,
            legal_weight=assignment.legal_weight, effective_from=assignment.effective_from,
            effective_to=assignment.effective_to, verification_status=assignment.verification_status,
            supersedes_assignment_id=assignment.supersedes_assignment_id,
        ))
        self._session.flush()

    def get(self, assignment_id: str) -> SourceAuthorityAssignment | None:
        row = self._session.get(SourceAuthorityAssignmentModel, assignment_id)
        if row is None:
            return None
        return SourceAuthorityAssignment(
            row.id, row.source_id, AuthorityType(row.authority_type), row.jurisdiction,
            row.domain, row.fact_type, row.precedence, row.legal_weight,
            row.effective_from, row.effective_to, row.verification_status,
            row.supersedes_assignment_id,
        )

    def list_for_source(self, source_id: str) -> list[SourceAuthorityAssignment]:
        rows = self._session.scalars(
            select(SourceAuthorityAssignmentModel)
            .where(SourceAuthorityAssignmentModel.source_id == source_id)
            .order_by(SourceAuthorityAssignmentModel.precedence, SourceAuthorityAssignmentModel.id)
        ).all()
        return [
            SourceAuthorityAssignment(
                row.id, row.source_id, AuthorityType(row.authority_type), row.jurisdiction,
                row.domain, row.fact_type, row.precedence, row.legal_weight,
                row.effective_from, row.effective_to, row.verification_status,
                row.supersedes_assignment_id,
            ) for row in rows
        ]


class SqlAlchemyInstrumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, instrument: Instrument) -> None:
        self._session.add(InstrumentModel(
            id=instrument.id, document_id=instrument.document_id,
            instrument_type=instrument.instrument_type.value,
            legal_effect=instrument.legal_effect.value, status=instrument.status.value,
            parties=list(instrument.parties),
            supersedes_instrument_id=instrument.supersedes_instrument_id,
        ))
        self._session.flush()

    def get(self, instrument_id: str) -> Instrument | None:
        row = self._session.get(InstrumentModel, instrument_id)
        return None if row is None else Instrument(
            row.id, row.document_id, InstrumentType(row.instrument_type),
            LegalEffect(row.legal_effect), InstrumentStatus(row.status), tuple(row.parties),
            row.supersedes_instrument_id,
        )

    def get_for_document(self, document_id: str) -> Instrument | None:
        row = self._session.scalars(
            select(InstrumentModel).where(InstrumentModel.document_id == document_id)
        ).first()
        return None if row is None else Instrument(
            row.id, row.document_id, InstrumentType(row.instrument_type),
            LegalEffect(row.legal_effect), row.status, tuple(row.parties),
            row.supersedes_instrument_id,
        )
