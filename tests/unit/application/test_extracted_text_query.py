from datetime import datetime, timezone

import pytest

from packages.application.source.extracted_text_query import GetExtractedText
from packages.domain.source.artifacts import ExtractedText


def extracted():
    return ExtractedText(
        "artifact-1",
        "extracted text",
        "extractor",
        "1.0",
        datetime(2026, 10, 2, tzinfo=timezone.utc),
    )


class TextRepo:
    def __init__(self, value=None):
        self.value = value

    def get(self, artifact_id):
        return self.value if self.value and self.value.artifact_id == artifact_id else None


def test_get_extracted_text():
    value = extracted()
    assert GetExtractedText(TextRepo(value)).execute("artifact-1") is value


def test_missing_extracted_text_is_rejected():
    with pytest.raises(ValueError, match="does not exist"):
        GetExtractedText(TextRepo()).execute("missing")
