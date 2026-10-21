from collections.abc import Mapping

from packages.application.requirement.revision_materializer import RequirementRevisionMaterializer
from packages.application.requirement.rule_tree_loader import RequirementRuleTreeLoader
from packages.application.scenarios.deterministic_applicability import DeterministicApplicabilityService
from packages.domain.scenario.models import ApplicabilityEvaluation


class RevisionAwareEvaluationService:
    def __init__(
        self,
        scenarios,
        rule_sets,
        memberships,
        revisions,
        rule_nodes,
        products,
        hs_codes,
        countries,
        markets,
        evidence,
        evaluations,
        traces,
    ) -> None:
        self.scenarios = scenarios
        self.rule_sets = rule_sets
        self.memberships = memberships
        self.revisions = revisions
        self.rule_nodes = rule_nodes
        self.materializer = RequirementRevisionMaterializer(products, hs_codes, countries, markets)
        self.evidence = evidence
        self.evaluations = evaluations
        self.traces = traces
        self.loader = RequirementRuleTreeLoader()
        self.evaluator = DeterministicApplicabilityService()

    def evaluate(self, scenario_id: str, facts: Mapping[str, object] | None = None):
        scenario = self.scenarios.get(scenario_id)
        if scenario is None:
            raise ValueError(f"Export scenario not found: {scenario_id}")
        rule_set = self.rule_sets.get_active()
        if rule_set is None:
            raise ValueError("No active rule set is configured")

        memberships = self.memberships.list_for_rule_set(rule_set.id)
        if not memberships:
            raise ValueError("Active rule set contains no requirement memberships")

        results = []
        for membership in memberships:
            revision = self.revisions.get(membership.requirement_revision)
            if revision is None:
                raise ValueError(f"Requirement revision does not exist: {membership.requirement_revision}")
            if revision.requirement_id != membership.requirement_id:
                raise ValueError("Rule-set membership and requirement revision disagree")
            requirement = self.materializer.materialize(revision)
            temporally_inactive = not requirement.is_effective_on(scenario.scenario_date)
            scope = requirement.scope_matches(
                scenario.product,
                scenario.hs_code,
                scenario.origin_country,
                scenario.destination_market,
            )
            # These are the only proven exclusions. Unknown scope remains
            # eligible for full evaluation so requirements are not omitted.
            if temporally_inactive or scope is False:
                evidence = ()
                tree = None
            else:
                evidence = tuple(
                    item
                    for evidence_id in requirement.evidence_ids
                    if (item := self.evidence.get(evidence_id)) is not None
                )
                # Rule nodes are immutable revision-scoped data. Loading by
                # the mutable requirement ID could mix different revisions.
                nodes = self.rule_nodes.list_for_revision(revision.id)
                tree = self.loader.load(requirement.id, revision.id, nodes) if nodes else None
            trace = self.evaluator.evaluate(
                scenario, requirement, evidence, tree, facts or {}
            )
            self.traces.add(trace, rule_set.version)
            evaluation = ApplicabilityEvaluation(
                scenario.id, requirement.id, trace.final_result, rule_set.version, evidence
            )
            self.evaluations.add(evaluation)
            results.append(evaluation)
        return results
