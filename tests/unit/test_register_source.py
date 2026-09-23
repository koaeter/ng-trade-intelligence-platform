from packages.application.source.register_source import RegisterSourceFromEndpoint
from packages.domain.source.authority_endpoint import AuthorityEndpoint
from packages.domain.source.models import Source

class EndpointRepo:
    def __init__(self, endpoint): self.endpoint = endpoint
    def get(self, endpoint_id): return self.endpoint if self.endpoint.id == endpoint_id else None

class SourceRepo:
    def __init__(self): self.items = []
    def add(self, source): self.items.append(source)

def test_registration_preserves_endpoint():
    endpoint = AuthorityEndpoint("nepc-documents", "nepc", "https://nepc.gov.ng/get-started/export-documents-procedures/", "EXPORT_PROCEDURES")
    repo = SourceRepo()
    source = RegisterSourceFromEndpoint(EndpointRepo(endpoint), repo).execute(Source("source-1", "NEPC Export Documents", "NEPC", "WEB_PAGE"), "nepc-documents")
    assert source.endpoint_id == "nepc-documents"
    assert source.official_url == endpoint.url
    assert repo.items == [source]

def test_registration_rejects_url_mismatch():
    endpoint = AuthorityEndpoint("nepc-documents", "nepc", "https://nepc.gov.ng/get-started/export-documents-procedures/", "EXPORT_PROCEDURES")
    try:
        RegisterSourceFromEndpoint(EndpointRepo(endpoint), SourceRepo()).execute(Source("source-1", "x", "NEPC", "WEB_PAGE", official_url="https://example.com"), "nepc-documents")
    except ValueError as exc:
        assert "URL" in str(exc)
    else:
        raise AssertionError("expected ValueError")
