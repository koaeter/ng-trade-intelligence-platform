import pytest

from packages.application.source.lifecycle import SourceLifecycleService
from packages.domain.source.models import Source, SourceStatus


def source(status):
    return Source("s1", "Source", "Authority", "GOVERNMENT", "NG", "https://example.gov", status)


def test_acquisition_transition_is_explicit():
    result = SourceLifecycleService().transition(source(SourceStatus.DISCOVERED), SourceStatus.ACQUIRED)
    assert result.status == SourceStatus.ACQUIRED


def test_cannot_publish_before_review():
    with pytest.raises(ValueError, match="Invalid source lifecycle"):
        SourceLifecycleService().transition(source(SourceStatus.EXTRACTED), SourceStatus.PUBLISHED)
