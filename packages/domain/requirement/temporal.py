from dataclasses import dataclass
from datetime import date

from packages.domain.requirement.evaluation import TruthValue


@dataclass(frozen=True)
class TemporalValidity:
    effective_from: date
    effective_to: date | None = None

    def evaluate(self, scenario_date: date) -> TruthValue:
        if scenario_date < self.effective_from:
            return TruthValue.FALSE
        if self.effective_to is not None and scenario_date >= self.effective_to:
            return TruthValue.FALSE
        return TruthValue.TRUE
