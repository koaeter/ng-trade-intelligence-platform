from datetime import date

from packages.domain.requirement.temporal import TemporalValidity


class TemporalRequirementEvaluator:
    def evaluate(self, validity: TemporalValidity, scenario_date: date) -> bool:
        return validity.evaluate(scenario_date).value == "TRUE"
