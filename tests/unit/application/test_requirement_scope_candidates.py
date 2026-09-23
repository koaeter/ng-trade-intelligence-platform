from datetime import date

import pytest

from packages.application.requirement.scope_candidates import RequirementScopeCandidateService


def test_scope_candidate_normalizes_structured_scope():
    result = RequirementScopeCandidateService().attach(
        "candidate-1",
        product_ids=("p2", "p1", "p1"),
        hs_codes=(("HS2022", "1801"), ("HS2022", "1801")),
        origin_country_codes=("ng", "NG"),
        destination_market_codes=("EU",),
        effective_from=date(2026, 1, 1),
        effective_to=date(2027, 1, 1),
        conditions=(" processing history ", ""),
    )

    assert result.product_ids == ("p1", "p2")
    assert result.hs_codes == (("HS2022", "1801"),)
    assert result.origin_country_codes == ("NG",)
    assert result.destination_market_codes == ("EU",)
    assert result.conditions == ("processing history",)


def test_scope_candidate_rejects_invalid_period():
    with pytest.raises(ValueError, match="effective_to"):
        RequirementScopeCandidateService().attach(
            "candidate-1",
            effective_from=date(2027, 1, 1),
            effective_to=date(2026, 1, 1),
        )
