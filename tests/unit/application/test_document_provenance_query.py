from packages.application.source.document_provenance_query import GetDocumentProvenance


class Item:
    def __init__(self, item_id, document_id, version_id=None):
        self.id = item_id
        self.document_id = document_id
        self.document_version_id = version_id


class MemoryVersions:
    def __init__(self, items):
        self.items = items

    def list_for_document(self, document_id):
        return [item for item in self.items if item.document_id == document_id]


class MemoryRelationships:
    def __init__(self, items):
        self.items = items

    def list_for_version(self, version_id):
        return [
            item
            for item in self.items
            if item.from_version_id == version_id
            or item.to_version_id == version_id
        ]


class MemoryArtifacts:
    def __init__(self, items):
        self.items = items

    def list_for_document_version(self, version_id):
        return [item for item in self.items if item.document_version_id == version_id]


def test_get_document_provenance_groups_artifacts_by_version():
    versions = [Item("v1", "document-1"), Item("v2", "document-1")]
    artifacts = [Item("a1", "document-1", "v1"), Item("a2", "document-1", "v2"), Item("a3", "document-1", "v1")]
    view = GetDocumentProvenance(
        MemoryVersions(versions),
        MemoryArtifacts(artifacts),
    ).execute("document-1")

    assert [version.id for version in view.versions] == ["v1", "v2"]
    assert [item.id for item in view.artifacts_by_version["v1"]] == ["a1", "a3"]
    assert [item.id for item in view.artifacts_by_version["v2"]] == ["a2"]
    assert [item.id for item in view.relationships_by_version["v1"]] == ["r1"]
    assert [item.id for item in view.relationships_by_version["v2"]] == ["r1"]