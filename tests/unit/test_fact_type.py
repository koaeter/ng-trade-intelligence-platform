from packages.domain.source.fact_type import FactType


def test_fact_type_is_a_governed_concept():
    fact_type = FactType("tariff", "Tariff", "TARIFF")
    assert fact_type.code == "TARIFF"
    assert fact_type.active
