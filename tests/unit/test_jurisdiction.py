from packages.domain.source.jurisdiction import Jurisdiction, JurisdictionType


def test_country_can_belong_to_a_regional_jurisdiction():
    ecowas = Jurisdiction("ecowas", "ECOWAS", JurisdictionType.REGIONAL, "ECOWAS")
    nigeria = Jurisdiction("ng", "Nigeria", JurisdictionType.COUNTRY, "NG", "ecowas")
    assert nigeria.parent_id == ecowas.id
    assert nigeria.jurisdiction_type is JurisdictionType.COUNTRY


def test_global_jurisdiction_has_no_parent():
    world = Jurisdiction("global", "Global", JurisdictionType.GLOBAL)
    assert world.parent_id is None
