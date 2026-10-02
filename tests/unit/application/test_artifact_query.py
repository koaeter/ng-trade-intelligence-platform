import pytest

from packages.application.source.artifact_query import GetSourceArtifact
from packages.domain.source.artifacts import ArtifactKind, SourceArtifact
from datetime import datetime, timezone


def artifact(artifact_id="artifact-1"):
    return SourceArtifact(
        artifact_id,
        "source-1",
        "document-1",
        ArtifactKind.PDF,
        "storage/key",
        "checksum",
        datetime(2026, 10, 2, tzinfo=timezone.utc),
    )


class ArtifactRepo:
    def __init__(self, value=None):
        self.value = value

    def get(self, artifact_id):
        return self.value if self.value and self.value.id == artifact_id else None


def test_get_source_artifact():
    value = artifact()
    assert GetSourceArtifact(ArtifactRepo(value)).execute("artifact-1") is value


def test_missing_source_artifact_is_rejected():
    with pytest.raises(ValueError, match="does not exist"):
        GetSourceArtifact(ArtifactRepo()).execute("missing")
