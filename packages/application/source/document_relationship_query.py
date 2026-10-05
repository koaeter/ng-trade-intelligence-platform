from packages.application.source.document_relationship_repositories import (
    DocumentRelationshipRepository,
)
from packages.domain.source.document_relationships import DocumentRelationship


class GetDocumentRelationship:
    """Read one explicit document-version relationship."""

    def __init__(self, relationships: DocumentRelationshipRepository) -> None:
        self.relationships = relationships

    def execute(self, relationship_id: str) -> DocumentRelationship:
        relationship = self.relationships.get(relationship_id)
        if relationship is None:
            raise ValueError("Document relationship does not exist")
        return relationship


class ListDocumentRelationships:
    """List relationships touching one document version."""

    def __init__(self, relationships: DocumentRelationshipRepository) -> None:
        self.relationships = relationships

    def execute(self, version_id: str, limit: int | None = None) -> list[DocumentRelationship]:
        return list(self.relationships.list_for_version(version_id, limit=limit))