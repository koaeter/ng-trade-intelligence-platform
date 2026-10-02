from packages.application.source.document_repositories import DocumentRepository
from packages.domain.source.models import Document


class GetDocument:
    """Read one immutable document identity."""

    def __init__(self, documents: DocumentRepository) -> None:
        self.documents = documents

    def execute(self, document_id: str) -> Document:
        document = self.documents.get(document_id)
        if document is None:
            raise ValueError("Document does not exist")
        return document
