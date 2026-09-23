from packages.application.source.repositories import SourceRepository
from packages.application.source.authority_endpoint_repositories import AuthorityEndpointRepository
from packages.domain.source.models import Source


class RegisterSourceFromEndpoint:
    def __init__(self, endpoint_repository: AuthorityEndpointRepository, source_repository: SourceRepository) -> None:
        self._endpoints = endpoint_repository
        self._sources = source_repository

    def execute(self, source: Source, endpoint_id: str) -> Source:
        endpoint = self._endpoints.get(endpoint_id)
        if endpoint is None or not endpoint.active:
            raise ValueError("Authority endpoint does not exist or is inactive")
        if source.endpoint_id not in (None, endpoint_id):
            raise ValueError("Source endpoint does not match registration endpoint")
        if source.official_url is not None and source.official_url != endpoint.url:
            raise ValueError("Source URL does not match registration endpoint")
        registered = Source(source.id, source.name, source.organization, source.source_type, source.jurisdiction, source.official_url or endpoint.url, source.status, endpoint_id)
        self._sources.add(registered)
        return registered
