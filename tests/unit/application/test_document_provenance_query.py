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


class MemoryDiffEntries:
    def __init__(self, items):
        self.items = items

    def list_for_diff(self, diff_id):
        return [item for item in self.items if item.diff_id == diff_id]


class MemoryDiffs:
    def __init__(self, items):
        self.items = items

    def list_for_comparison(self, comparison_id):
        return [
            item for item in self.items if item.comparison_id == comparison_id
        ]


class MemoryComparisons:
    def __init__(self, items):
        self.items = items

    def list_for_extraction(self, extraction_id):
        return [
            item
            for item in self.items
            if item.baseline_extraction_id == extraction_id
            or item.candidate_extraction_id == extraction_id
        ]


class MemorySegments:
    def __init__(self, items):
        self.items = items

    def list_for_extraction(self, extraction_id):
        return [
            item for item in self.items if item.extraction_id == extraction_id
        ]


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


class MemoryExtractions:
    def __init__(self, items):
        self.items = items

    def list_for_artifact(self, artifact_id):
        return [
            item for item in self.items if item.artifact_id == artifact_id
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
    assert [item.id for item in view.extraction_runs_by_artifact["a1"]] == ["e1"]
    assert [item.id for item in view.segments_by_extraction["e1"]] == ["s1"]
    assert [item.id for item in view.comparisons_by_extraction["e1"]] == ["c1"]
    assert [item.id for item in view.diffs_by_comparison["c1"]] == ["d1"]
    assert [item.id for item in view.diff_entries_by_diff["d1"]] == ["de1"]