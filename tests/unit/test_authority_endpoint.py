from packages.application.source.authority_endpoint_seed import INITIAL_NIGERIAN_AUTHORITY_ENDPOINTS
from packages.domain.source.authority_endpoint import AuthorityEndpoint


def test_endpoint_belongs_to_registered_authority():
    endpoint = AuthorityEndpoint("x", "ncs", "https://www.customs.gov.ng/", "OFFICIAL_PORTAL")
    assert endpoint.authority_id == "ncs"
    assert endpoint.access_method == "HTTPS_WEB"


def test_nigerian_endpoint_seed_has_unique_urls_per_authority():
    keys = [(x.authority_id, x.url) for x in INITIAL_NIGERIAN_AUTHORITY_ENDPOINTS]
    assert len(keys) == len(set(keys))


def test_endpoint_seed_covers_initial_authorities():
    authorities = {x.authority_id for x in INITIAL_NIGERIAN_AUTHORITY_ENDPOINTS}
    assert {"nepc", "ncs", "son", "nafdac", "naqs", "ninas"} <= authorities
