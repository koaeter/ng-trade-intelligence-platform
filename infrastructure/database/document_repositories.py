from packages.domain.source.models import Document


class SqlAlchemyDocumentRepository:
    def __init__(self, session) -> None:
        self._session = session

    def add(self, document: Document) -> None:
        from infrastructure.database.models import DocumentModel
        self._session.add(DocumentModel(
            id=document.id,
            source_id=document.source_id,
            title=document.title,
            document_type=document.document_type,
            publication_date=document.publication_date,
            effective_from=document.effective_from,
            effective_to=document.effective_to,
            version_label=document.version_label,
        ))
        self._session.flush()

    def get(self, document_id: str) -> Document | None:
        from infrastructure.database.models import DocumentModel
        row = self._session.get(DocumentModel, document_id)
        if row is None:
            return None
        return Document(
            row.id, row.source_id, row.title, row.document_type,
            row.publication_date, row.effective_from, row.effective_to, row.version_label,
        )
