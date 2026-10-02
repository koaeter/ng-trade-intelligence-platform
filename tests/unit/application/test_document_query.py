from datetime import date

import pytest

from packages.application.source.document_query import GetDocument
from packages.domain.source.models import Document


def document(document_id="document-1"):
    return Document(document_id, "source-1", "Regulation", "REGULATION", date(2026, 10, 1))


class DocumentRepo:
    def __init__(self, value=None):
        self.value = value

    def get(self, document_id):
        return self.value if self.value and self.value.id == document_id else None


def test_get_document():
    value = document()
    assert GetDocument(DocumentRepo(value)).execute("document-1") is value


def test_missing_document_is_rejected():
    with pytest.raises(ValueError, match="does not exist"):
        GetDocument(DocumentRepo()).execute("missing")
