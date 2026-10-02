from packages.application.source.document_relationship_query import GetDocumentRelationship, ListDocumentRelationships
from packages.domain.source.document_relationships import DocumentRelationship, DocumentRelationshipType


class MemoryRelationships:
    def __init__(self):
        self.items = {}

    def add(self, value):
        self.items[value.id] = value

    def get(self, key):
        return self.items.get(key)

    def list_for_version(self, version_id):
        return [
            value for value in self.items.values()
            if value.from_version_id == version_id or value.to_version_id == version_id
        ]


def test_get_document_relationship_returns_relationship():
    repo = MemoryRelationships()
    relationship = DocumentRelationship("r1", DocumentRelationshipType.SUPERSEDES, "v2", "v1")
    repo.add(relationship)
    assert GetDocumentRelationship(repo).execute("r1") == relationship


def test_get_document_relationship_rejects_missing_relationship():
    import pytest
    with pytest.raises(ValueError, match="does not exist"):
        GetDocumentRelationship(MemoryRelationships()).execute("missing")


def test_list_document_relationships_returns_touching_relationships():
    repo = MemoryRelationships()
    repo.add(DocumentRelationship("r1", DocumentRelationshipType.SUPERSEDES, "v2", "v1"))
    repo.add(DocumentRelationship("r2", DocumentRelationshipType.AMENDS, "v3", "v2"))
    repo.add(DocumentRelationship("r3", DocumentRelationshipType.ANNEX_OF, "v4", "v5"))
    result = ListDocumentRelationships(repo).execute("v2")
    assert [x.id for x in result] == ["r1", "r2"]