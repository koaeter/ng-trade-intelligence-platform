from packages.domain.source.authority_registry import Authority


def test_authority_is_scoped_to_a_jurisdiction():
    authority = Authority("nepc", "Nigerian Export Promotion Council", "NEPC", "ng", "EXPORT_PROMOTION")
    assert authority.jurisdiction_id == "ng"
    assert authority.acronym == "NEPC"
