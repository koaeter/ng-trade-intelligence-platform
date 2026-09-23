from collections.abc import Mapping

from packages.application.requirement.rule_tree_evaluator import RequirementRuleTreeEvaluator
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.requirement.evaluation import TruthValue
from packages.domain.requirement.rule_tree import ConditionNode
from packages.domain.scenario.applicability_trace import ApplicabilityTrace
from packages.domain.scenario.models import EvaluationResult, ExportScenario


class DeterministicApplicabilityService:
    def __init__(self) -> None:
        self.rule_tree = RequirementRuleTreeEvaluator()

    def evaluate(
        self,
        scenario: ExportScenario,
        requirement: Requirement,
        evidence: tuple[Evidence, ...] = (),
        condition_tree: ConditionNode | None = None,
        facts: Mapping[str, object] | None = None,
    ) -> ApplicabilityTrace:
        temporal = (
            TruthValue.TRUE
            if requirement.is_effective_on(scenario.scenario_date)
            else TruthValue.FALSE
        )
        if temporal == TruthValue.FALSE:
            final = EvaluationResult.NOT_APPLICABLE
            return self._trace(scenario, requirement, temporal, TruthValue.UNKNOWN, TruthValue.UNKNOWN, evidence, final)

        scope = requirement.scope_matches(
            scenario.product, scenario.hs_code, scenario.origin_country, scenario.destination_market
        )
        scope_value = TruthValue.TRUE if (
            scope is True or (scope is None and requirement.scope_is_general)
        ) else TruthValue.FALSE if scope is False else TruthValue.UNKNOWN
        if scope_value == TruthValue.FALSE:
            final = EvaluationResult.NOT_APPLICABLE
            return self._trace(scenario, requirement, temporal, scope_value, TruthValue.UNKNOWN, evidence, final)
        if scope_value == TruthValue.UNKNOWN:
            final = EvaluationResult.UNRESOLVED
            return self._trace(scenario, requirement, temporal, scope_value, TruthValue.UNKNOWN, evidence, final)

        condition_value = TruthValue.TRUE
        if condition_tree is not None:
            condition_value = self.rule_tree.evaluate(condition_tree, facts or {}).result
        if condition_value == TruthValue.FALSE:
            final = EvaluationResult.NOT_APPLICABLE
            return self._trace(scenario, requirement, temporal, scope_value, condition_value, evidence, final)
        if condition_value == TruthValue.UNKNOWN:
            final = EvaluationResult.UNRESOLVED
            return self._trace(scenario, requirement, temporal, scope_value, condition_value, evidence, final)

        if not evidence:
            final = EvaluationResult.INSUFFICIENT_EVIDENCE
        elif not all(item.verified for item in evidence):
            final = EvaluationResult.UNRESOLVED
        else:
            final = EvaluationResult.APPLICABLE
        return self._trace(scenario, requirement, temporal, scope_value, condition_value, evidence, final)

    @staticmethod
    def _trace(scenario, requirement, temporal, scope, condition, evidence, final):
        evidence_result = (
            EvaluationResult.INSUFFICIENT_EVIDENCE if not evidence
            else EvaluationResult.APPLICABLE if all(item.verified for item in evidence)
            else EvaluationResult.UNRESOLVED
        )
        return ApplicabilityTrace(
            scenario.id,
            requirement.id,
            scenario.scenario_date,
            temporal,
            scope,
            condition,
            evidence_result,
            final,
        )
