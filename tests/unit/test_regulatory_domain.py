from packages.domain.source.regulatory_domain import RegulatoryDomain


def test_regulatory_domain_supports_hierarchy():
    trade = RegulatoryDomain("trade", "Trade", "TRADE")
    customs = RegulatoryDomain("customs", "Customs", "CUSTOMS", parent_id=trade.id)
    assert customs.parent_id == "trade"
    assert customs.code == "CUSTOMS"
