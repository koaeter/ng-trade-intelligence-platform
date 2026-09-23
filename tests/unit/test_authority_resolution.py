from datetime import date
from packages.domain.source.authority import AuthorityType, SourceAuthorityAssignment
from packages.domain.source.authority_resolution import resolve_authority


def assignment(identifier: str, precedence: int, weight: int) -> SourceAuthorityAssignment:
    return SourceAuthorityAssignment(
        identifier, "source", AuthorityType.PRIMARY_LEGAL, "NG", "CUSTOMS", "TARIFF",
        precedence, weight, date(2026, 1, 1), None, "VERIFIED",
    )


def test_resolution_selects_highest_precedence():
    result = resolve_authority([assignment("low", 20, 80), assignment("high", 10, 70)], date(2026, 9, 23))
    assert result.status == "RESOLVED"
    assert result.selected.id == "high"


def test_equal_precedence_and_weight_is_not_silently_overridden():
    result = resolve_authority([assignment("a", 10, 90), assignment("b", 10, 90)], date(2026, 9, 23))
    assert result.status == "CONFLICT"
    assert result.selected is None


def test_unverified_authority_is_not_selected():
    item = assignment("unverified", 1, 100)
    item = SourceAuthorityAssignment(
        item.id, item.source_id, item.authority_type, item.jurisdiction, item.domain,
        item.fact_type, item.precedence, item.legal_weight, item.effective_from,
        item.effective_to, "UNVERIFIED",
    )
    result = resolve_authority([item], date(2026, 9, 23))
    assert result.status == "UNRESOLVED"
