import pytest

from packages.application.source.extraction_diff_query import GetExtractionDiff, ListExtractionDiffs
from packages.domain.source.extraction_diff import ExtractionDiff


def diff(diff_id="diff-1", comparison_id="cmp-1"):
    return ExtractionDiff(diff_id, comparison_id, "run-a", "run-b", 0, 0, 0, 0, 0, None)


class DiffRepo:
    def __init__(self, values=None): self.values = values or []
    def get(self, diff_id):
        return next((x for x in self.values if x.id == diff_id), None)
    def list_for_comparison(self, comparison_id, limit=None):
        return [x for x in self.values if x.comparison_id == comparison_id]


class EntryRepo:
    def __init__(self, values=None): self.values = values or []
    def list_for_diff(self, diff_id, limit=None):
        return [x for x in self.values if x.diff_id == diff_id]


def test_get_returns_entries_in_ordinal_order():
    d = diff()
    entries = [type("E", (), {"diff_id":"diff-1", "ordinal":2})(),
               type("E", (), {"diff_id":"diff-1", "ordinal":0})(),
               type("E", (), {"diff_id":"diff-1", "ordinal":1})()]
    got, result = GetExtractionDiff(DiffRepo([d]), EntryRepo(entries)).execute("diff-1")
    assert got is d
    assert [x.ordinal for x in result] == [0, 1, 2]


def test_missing_diff_is_rejected():
    with pytest.raises(ValueError, match="does not exist"):
        GetExtractionDiff(DiffRepo(), EntryRepo()).execute("missing")


def test_list_scopes_by_comparison():
    values = [diff("d1", "cmp-1"), diff("d2", "cmp-2"), diff("d3", "cmp-1")]
    result = ListExtractionDiffs(DiffRepo(values)).execute("cmp-1")
    assert [x.id for x in result] == ["d1", "d3"]