from datetime import datetime, timezone

from packages.application.source.authority_endpoint_repositories import AuthorityEndpointRepository
from packages.application.source.source_acquisition import SourceFetcher
from packages.domain.source.authority_endpoint import AuthorityEndpoint, EndpointVerificationStatus


class VerifyAuthorityEndpoint:
    def __init__(self, endpoints: AuthorityEndpointRepository) -> None:
        self.endpoints = endpoints

    def execute(self, endpoint_id: str, fetcher: SourceFetcher) -> AuthorityEndpoint:
        endpoint = self.endpoints.get(endpoint_id)
        if endpoint is None:
            raise ValueError("Authority endpoint does not exist")
        now = datetime.now(timezone.utc)
        try:
            fetcher.fetch(endpoint.url)
        except Exception as exc:
            updated = AuthorityEndpoint(
                endpoint.id, endpoint.authority_id, endpoint.url, endpoint.endpoint_type,
                endpoint.access_method, endpoint.content_format, endpoint.purpose, endpoint.active,
                EndpointVerificationStatus.FAILED, now, str(exc)[:2000],
            )
            self.endpoints.update(updated)
            raise
        updated = AuthorityEndpoint(
            endpoint.id, endpoint.authority_id, endpoint.url, endpoint.endpoint_type,
            endpoint.access_method, endpoint.content_format, endpoint.purpose, endpoint.active,
            EndpointVerificationStatus.VERIFIED, now, None,
        )
        self.endpoints.update(updated)
        return updated
