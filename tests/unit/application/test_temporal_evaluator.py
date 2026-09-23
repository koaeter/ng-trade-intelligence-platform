from datetime import date

from packages.application.requirement.temporal_evaluator import TemporalRequirementEvaluator
from packages.domain.requirement.temporal import TemporalValidity


def test_rule_is_effective_on_start_date():
    rule = TemporalValidity(date(2026, 1, 1), date(2027, 1, 1))
    assert TemporalRequirementEvaluator().evaluate(rule, date(2026, 1, 1))


def test_rule_is_not_effective_after_exclusive_end():
    rule = TemporalValidity(date(2026, 1, 1), date(2027, 1, 1))
    assert not TemporalRequirementEvaluator().evaluate(rule, date(2027, 1, 1))


def test_rule_is_not_effective_before_start():
    rule = TemporalValidity(date(2026, 1, 1))
    assert not TemporalRequirementEvaluator().evaluate(rule, date(2025, 12, 31))
