from packages.application.source.document_repositories import DocumentRepository
from packages.application.source.register_source import RegisterSourceFromEndpoint
from packages.domain.source.models import Document


class RegisterDocument:
    def __init__(self, documents: DocumentRepository) -> None:
        self.documents = documents

    def execute(self, document: Document) -> Document:
        if not document.source_id:
            raise ValueError("Document must reference a source")
        if not document.title.strip():
            raise ValueError("Document title is required")
        if not document.document_type.strip():
            raise ValueError("Document type is required")
        if self.documents.get(document.id) is not None:
            raise ValueError("Document already exists")
        self.documents.add(document)
        return document
