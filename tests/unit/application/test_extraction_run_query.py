from datetime import datetime, timezone

import pytest

from packages.application.source.extraction_run_query import (
    GetExtractionRun,
    ListExtractionRunsForArtifact,
)
from packages.domain.source.extraction import ExtractionRun


def extraction(extraction_id="run-1", artifact_id="artifact-1"):
    return ExtractionRun(
        extraction_id,
        artifact_id,
        "version-1",
        "input",
        "extractor",
        "1.0",
        datetime(2026, 10, 2, tzinfo=timezone.utc),
    )


class RunRepo:
    def __init__(self, values=None):
        self.values = values or []

    def get(self, extraction_id):
        return next((x for x in self.values if x.id == extraction_id), None)

    def list_for_artifact(self, artifact_id, limit=None):
        return [x for x in self.values if x.artifact_id == artifact_id]


def test_get_extraction_run():
    value = extraction()
    assert GetExtractionRun(RunRepo([value])).execute("run-1") is value


def test_missing_extraction_run_is_rejected():
    with pytest.raises(ValueError, match="does not exist"):
        GetExtractionRun(RunRepo()).execute("missing")


def test_list_extraction_runs_scopes_to_artifact():
    values = [extraction("run-1", "a"), extraction("run-2", "b"), extraction("run-3", "a")]
    result = ListExtractionRunsForArtifact(RunRepo(values)).execute("a")
    assert [x.id for x in result] == ["run-1", "run-3"]
