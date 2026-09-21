from datetime import date

from packages.domain.requirement.models import Requirement


def test_requirement_is_effective_on_date_inside_period() -> None:
    requirement = Requirement(
        id="req-1",
        name="Sample export requirement",
        effective_from=date(2026, 1, 1),
    )

    assert requirement.is_effective_on(date(2026, 9, 21))


def test_requirement_is_not_effective_before_start() -> None:
    requirement = Requirement(
        id="req-1",
        name="Sample export requirement",
        effective_from=date(2026, 1, 1),
    )

    assert not requirement.is_effective_on(date(2025, 12, 31))
