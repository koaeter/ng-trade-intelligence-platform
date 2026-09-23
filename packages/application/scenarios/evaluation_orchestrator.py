from collections.abc import Mapping

from packages.application.requirement.rule_tree_loader import RequirementRuleTreeLoader
from packages.application.scenarios.deterministic_applicability import DeterministicApplicabilityService
from packages.domain.scenario.models import ApplicabilityEvaluation, ExportScenario


RULE_SET_VERSION = "initial"


class ScenarioEvaluationOrchestrator:
    """Evaluates requirements and persists both result and deterministic trace."""

    def __init__(
        self,
        scenarios,
        requirements,
        evaluations,
        evidence,
        rule_nodes,
        traces,
    ) -> None:
        self.scenarios = scenarios
        self.requirements = requirements
        self.evaluations = evaluations
        self.evidence = evidence
        self.rule_nodes = rule_nodes
        self.traces = traces
        self.loader = RequirementRuleTreeLoader()
        self.evaluator = DeterministicApplicabilityService()

    def evaluate(self, scenario_id: str, facts: Mapping[str, object] | None = None):
        scenario = self.scenarios.get(scenario_id)
        if scenario is None:
            raise ValueError(f"Export scenario not found: {scenario_id}")

        results = []
        for requirement in self.requirements.list_all():
            evidence = tuple(
                item
                for evidence_id in requirement.evidence_ids
                if (item := self.evidence.get(evidence_id)) is not None
            )
            nodes = self.rule_nodes.list_for_requirement(requirement.id)
            tree = self.loader.load(requirement.id, nodes) if nodes else None
            trace = self.evaluator.evaluate(
                scenario,
                requirement,
                evidence,
                tree,
                facts or {},
            )
            self.traces.add(trace, RULE_SET_VERSION)
            results.append(
                ApplicabilityEvaluation(
                    scenario.id,
                    requirement.id,
                    trace.final_result,
                    RULE_SET_VERSION,
                    evidence,
                )
            )
            self.evaluations.add(results[-1])
        return results
