from packages.application.source.regulatory_source_seed import INITIAL_NIGERIAN_REGULATORY_SOURCES


def test_initial_nigerian_sources_are_endpoint_bound():
    assert INITIAL_NIGERIAN_REGULATORY_SOURCES
    assert all(source.endpoint_id for source in INITIAL_NIGERIAN_REGULATORY_SOURCES)


def test_initial_nigerian_sources_have_official_urls():
    assert all(source.official_url and source.official_url.startswith("https://") for source in INITIAL_NIGERIAN_REGULATORY_SOURCES)
