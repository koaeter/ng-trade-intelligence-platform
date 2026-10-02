from datetime import date

import pytest

from packages.application.source.document_version_query import GetDocumentVersion, ListDocumentVersions
from packages.domain.source.document_versions import DocumentVersion


def version(version_id="version-1", document_id="document-1"):
    return DocumentVersion(version_id, document_id, "v1", date(2026, 10, 2))


class VersionRepo:
    def __init__(self, values=None):
        self.values = values or []

    def get(self, version_id):
        return next((x for x in self.values if x.id == version_id), None)

    def list_for_document(self, document_id):
        return [x for x in self.values if x.document_id == document_id]


def test_get_document_version():
    value = version()
    assert GetDocumentVersion(VersionRepo([value])).execute("version-1") is value


def test_missing_document_version_is_rejected():
    with pytest.raises(ValueError, match="does not exist"):
        GetDocumentVersion(VersionRepo()).execute("missing")


def test_list_document_versions_scopes_to_document():
    values = [version("v1", "d1"), version("v2", "d2"), version("v3", "d1")]
    result = ListDocumentVersions(VersionRepo(values)).execute("d1")
    assert [x.id for x in result] == ["v1", "v3"]
