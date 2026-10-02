from packages.application.source.document_version_artifact_query import ListSourceArtifactsForDocumentVersion


class MemoryArtifacts:
    def __init__(self):
        self.items = []

    def add(self, value):
        self.items.append(value)

    def list_for_document_version(self, version_id):
        return [value for value in self.items if value.document_version_id == version_id]


class Artifact:
    def __init__(self, artifact_id, version_id):
        self.id = artifact_id
        self.document_version_id = version_id


def test_list_source_artifacts_for_document_version():
    repo = MemoryArtifacts()
    repo.add(Artifact("a1", "v1"))
    repo.add(Artifact("a2", "v2"))
    repo.add(Artifact("a3", "v1"))
    result = ListSourceArtifactsForDocumentVersion(repo).execute("v1")
    assert [item.id for item in result] == ["a1", "a3"]