import pytest

from packages.application.source.register_document_relationship import RegisterDocumentRelationship
from packages.domain.source.document_relationships import DocumentRelationship, DocumentRelationshipType
from packages.domain.source.document_versions import DocumentVersion


class MemoryVersions:
    def __init__(self):
        self.items = {}

    def add(self, value):
        self.items[value.id] = value

    def get(self, key):
        return self.items.get(key)


class MemoryRelationships:
    def __init__(self):
        self.items = {}

    def add(self, value):
        self.items[value.id] = value

    def get(self, key):
        return self.items.get(key)


def versions():
    repo = MemoryVersions()
    repo.add(DocumentVersion("v1", "doc1"))
    repo.add(DocumentVersion("v2", "doc1"))
    return repo


def test_relationship_requires_existing_versions():
    with pytest.raises(ValueError, match="existing document versions"):
        RegisterDocumentRelationship(
            MemoryRelationships(), versions()
        ).execute(
            DocumentRelationship(
                "r1", DocumentRelationshipType.SUPERSEDES, "v1", "missing"
            )
        )


def test_relationship_rejects_self_reference():
    with pytest.raises(ValueError, match="same version"):
        RegisterDocumentRelationship(
            MemoryRelationships(), versions()
        ).execute(
            DocumentRelationship(
                "r1", DocumentRelationshipType.AMENDS, "v1", "v1"
            )
        )


def test_verified_relationship_requires_evidence():
    with pytest.raises(ValueError, match="evidence reference"):
        RegisterDocumentRelationship(
            MemoryRelationships(), versions()
        ).execute(
            DocumentRelationship(
                "r1", DocumentRelationshipType.SUPERSEDES, "v2", "v1",
                verified=True
            )
        )


def test_valid_unverified_relationship_can_be_registered():
    relationships = MemoryRelationships()
    relationship = DocumentRelationship(
        "r1", DocumentRelationshipType.SUPERSEDES, "v2", "v1"
    )
    assert RegisterDocumentRelationship(
        relationships, versions()
    ).execute(relationship) == relationship
