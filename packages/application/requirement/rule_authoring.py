from uuid import uuid4

from packages.domain.requirement.conditions import RequirementConditionCandidate
from packages.domain.requirement.rule_nodes import RequirementRuleNode, RequirementRuleNodeType
from packages.domain.requirement.rule_tree import ConditionGroup, ConditionLeaf, ConditionNode


class RequirementRuleAuthoringService:
    def __init__(self, memberships, rule_nodes) -> None:
        self.memberships = memberships
        self.rule_nodes = rule_nodes

    def add_tree(
        self,
        rule_set_id: str,
        requirement_id: str,
        revision_id: str,
        tree: ConditionNode,
    ) -> list[RequirementRuleNode]:
        memberships = self.memberships.list_for_rule_set(rule_set_id)
        if not any(
            item.requirement_id == requirement_id
            and item.requirement_revision == revision_id
            for item in memberships
        ):
            raise ValueError("Requirement revision is not a member of the rule set")

        nodes: list[RequirementRuleNode] = []

        def visit(node: ConditionNode, parent_id: str | None, sequence: int) -> str:
            node_id = str(uuid4())
            if isinstance(node, ConditionLeaf):
                candidate: RequirementConditionCandidate = node.condition
                record = RequirementRuleNode(
                    node_id,
                    requirement_id,
                    revision_id,
                    parent_id,
                    sequence,
                    RequirementRuleNodeType.CONDITION,
                    field=candidate.field,
                    operator=candidate.operator,
                    value=candidate.value,
                )
                nodes.append(record)
                self.rule_nodes.add(record)
                return node_id

            record = RequirementRuleNode(
                node_id,
                requirement_id,
                revision_id,
                parent_id,
                sequence,
                RequirementRuleNodeType.GROUP,
                group_operator=node.operator,
            )
            nodes.append(record)
            self.rule_nodes.add(record)
            for child_sequence, child in enumerate(node.children):
                visit(child, node_id, child_sequence)
            return node_id

        visit(tree, None, 0)
        return nodes
