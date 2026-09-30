from datetime import date

import pytest

from packages.application.source.register_document_version import RegisterDocumentVersion
from packages.domain.source.document_versions import DocumentVersion
from packages.domain.source.models import Document


class MemoryDocuments:
    def __init__(self):
        self.items = {}

    def add(self, document):
        self.items[document.id] = document

    def get(self, document_id):
        return self.items.get(document_id)


class MemoryVersions:
    def __init__(self):
        self.items = {}

    def add(self, version):
        self.items[version.id] = version

    def get(self, version_id):
        return self.items.get(version_id)

    def list_for_document(self, document_id):
        return [x for x in self.items.values() if x.document_id == document_id]


def test_document_version_requires_existing_document():
    documents = MemoryDocuments()
    versions = MemoryVersions()
    service = RegisterDocumentVersion(versions, documents)

    with pytest.raises(ValueError, match="existing document"):
        service.execute(DocumentVersion("v1", "missing"))


def test_document_version_is_immutable_and_registered_once():
    documents = MemoryDocuments()
    documents.add(Document("doc1", "src1", "Export Guide", "GUIDE"))
    versions = MemoryVersions()
    service = RegisterDocumentVersion(versions, documents)

    version = DocumentVersion(
        "v1", "doc1", "2026 edition",
        date(2026, 1, 1), date(2026, 1, 1), None, "REF-2026",
    )
    assert service.execute(version) == version

    with pytest.raises(ValueError, match="already exists"):
        service.execute(version)


def test_document_version_rejects_invalid_effective_interval():
    documents = MemoryDocuments()
    documents.add(Document("doc1", "src1", "Export Guide", "GUIDE"))
    service = RegisterDocumentVersion(MemoryVersions(), documents)

    with pytest.raises(ValueError, match="effective_to"):
        service.execute(
            DocumentVersion(
                "v1", "doc1", "bad",
                effective_from=date(2026, 2, 1),
                effective_to=date(2026, 2, 1),
            )
        )
