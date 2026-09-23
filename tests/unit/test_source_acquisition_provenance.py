from datetime import datetime, timezone
from packages.application.source.source_acquisition import TrackedSourceAcquisitionService, AcquiredSourceResponse
from packages.domain.source.models import Source
from packages.domain.source.acquisition import AcquisitionEventStatus


class EventRepo:
    def __init__(self): self.events = {}
    def add(self, event): self.events[event.id] = event
    def get(self, event_id): return self.events.get(event_id)
    def link_artifact(self, event_id, artifact_id):
        event = self.events[event_id]
        from dataclasses import replace
        self.events[event_id] = replace(event, artifact_id=artifact_id)


class Fetcher:
    def __init__(self, response=None, error=None): self.response, self.error = response, error
    def fetch(self, url):
        if self.error: raise self.error
        return self.response


def source():
    return Source("s1", "NEPC", "NEPC", "OFFICIAL", official_url="https://nepc.gov.ng/x", endpoint_id="ep1")


def test_success_records_hash_and_endpoint():
    repo = EventRepo()
    response = AcquiredSourceResponse("https://nepc.gov.ng/x", "text/html", b"abc", 200, "https://nepc.gov.ng/x")
    result, event_id = TrackedSourceAcquisitionService(repo).acquire(source(), Fetcher(response), user_agent="test-agent")
    event = repo.get(event_id)
    assert result == response
    assert event.status is AcquisitionEventStatus.SUCCEEDED
    assert event.endpoint_id == "ep1"
    assert event.content_length == 3
    assert event.response_sha256 == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert event.user_agent == "test-agent"


def test_failure_is_persisted():
    repo = EventRepo()
    try:
        TrackedSourceAcquisitionService(repo).acquire(source(), Fetcher(error=ValueError("blocked")))
    except ValueError:
        pass
    else:
        raise AssertionError("expected acquisition failure")
    event = next(iter(repo.events.values()))
    assert event.status is AcquisitionEventStatus.FAILED
    assert event.error_code == "ValueError"
    assert event.error_message == "blocked"
    assert event.artifact_id is None
