from packages.application.source.document_provenance_query import GetDocumentProvenance


class Item:
    def __init__(self, item_id, document_id=None, version_id=None, **kwargs):
        self.id = item_id
        self.document_id = document_id
        self.document_version_id = version_id
        for key, value in kwargs.items():
            setattr(self, key, value)


class Memory:
    def __init__(self, items): self.items = items
    def list_for_document(self, document_id):\n        return [x for x in self.items if x.document_id == document_id]
    def list_for_document_version(self, version_id):\n        return [x for x in self.items if x.document_version_id == version_id]
    def list_for_version(self, version_id):\n        return [\n            x for x in self.items\n            if x.from_version_id == version_id or x.to_version_id == version_id\n        ]
    def list_for_artifact(self, artifact_id):\n        return [x for x in self.items if x.artifact_id == artifact_id]
    def list_for_extraction(self, extraction_id):\n        return [\n            x for x in self.items\n            if getattr(x, "extraction_id", None) == extraction_id\n            or getattr(x, "baseline_extraction_id", None) == extraction_id\n            or getattr(x, "candidate_extraction_id", None) == extraction_id\n        ]
    def list_for_comparison(self, comparison_id):\n        return [x for x in self.items if x.comparison_id == comparison_id]
    def list_for_diff(self, diff_id): return [x for x in self.items if x.diff_id == diff_id]


def test_get_document_provenance_builds_complete_processing_chain():
    versions = [Item("v1", "document-1"), Item("v2", "document-1")]
    artifacts = [\n        Item("a1", "document-1", "v1"),\n        Item("a2", "document-1", "v2"),\n        Item("a3", "document-1", "v1"),\n    ]
    relationships = [Item("r1", from_version_id="v1", to_version_id="v2")]
    extractions = [Item("e1", artifact_id="a1")]
    segments = [Item("s1", extraction_id="e1")]
    comparisons = [Item("c1", baseline_extraction_id="e1", candidate_extraction_id="e2")]
    diffs = [Item("d1", comparison_id="c1")]
    entries = [Item("de1", diff_id="d1")]

    view = GetDocumentProvenance(
        Memory(versions), Memory(artifacts), Memory(relationships), Memory(extractions),
        Memory(segments), Memory(comparisons), Memory(diffs), Memory(entries),
    ).execute("document-1")

    assert [x.id for x in view.versions] == ["v1", "v2"]
    assert [x.id for x in view.artifacts_by_version["v1"]] == ["a1", "a3"]
    assert [x.id for x in view.artifacts_by_version["v2"]] == ["a2"]
    assert [x.id for x in view.relationships_by_version["v1"]] == ["r1"]
    assert [x.id for x in view.extraction_runs_by_artifact["a1"]] == ["e1"]
    assert [x.id for x in view.segments_by_extraction["e1"]] == ["s1"]
    assert [x.id for x in view.comparisons_by_extraction["e1"]] == ["c1"]
    assert [x.id for x in view.diffs_by_comparison["c1"]] == ["d1"]
    assert [x.id for x in view.diff_entries_by_diff["d1"]] == ["de1"]
