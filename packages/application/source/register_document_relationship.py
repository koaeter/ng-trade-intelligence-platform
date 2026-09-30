from packages.application.source.document_version_repositories import DocumentVersionRepository
from packages.application.source.document_relationship_repositories import DocumentRelationshipRepository
from packages.domain.source.document_relationships import DocumentRelationship


class RegisterDocumentRelationship:
    def __init__(
        self,
        relationships: DocumentRelationshipRepository,
        versions: DocumentVersionRepository,
    ) -> None:
        self.relationships = relationships
        self.versions = versions

    def execute(self, relationship: DocumentRelationship) -> DocumentRelationship:
        if self.relationships.get(relationship.id) is not None:
            raise ValueError("Document relationship already exists")
        source = self.versions.get(relationship.from_version_id)
        target = self.versions.get(relationship.to_version_id)
        if source is None or target is None:
            raise ValueError("Document relationship must reference existing document versions")
        if source.id == target.id:
            raise ValueError("Document relationship cannot reference the same version")
        if relationship.verified and not relationship.evidence_reference:
            raise ValueError("Verified document relationship requires evidence reference")
        if relationship.note is not None and not relationship.note.strip():
            raise ValueError("Document relationship note cannot be blank")
        self.relationships.add(relationship)
        return relationship
