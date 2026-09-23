from packages.domain.requirement.rule_nodes import RequirementRuleNode, RequirementRuleNodeType
from packages.domain.requirement.rule_tree import ConditionGroup, ConditionLeaf, ConditionNode


class RequirementRuleTreeLoader:
    def load(self, requirement_id: str, nodes: list[RequirementRuleNode]) -> ConditionNode:
        if not nodes:
            raise ValueError("Requirement has no rule tree")
        by_id = {node.id: node for node in nodes}
        if len(by_id) != len(nodes):
            raise ValueError("Requirement rule tree contains duplicate node IDs")

        for node in nodes:
            if node.requirement_id != requirement_id:
                raise ValueError("Requirement rule node references another requirement")
            if node.parent_id is not None and node.parent_id not in by_id:
                raise ValueError("Requirement rule node references a missing parent")

        roots = [node for node in nodes if node.parent_id is None]
        if len(roots) != 1:
            raise ValueError("Requirement rule tree must have exactly one root")

        children = {}
        for node in nodes:
            children.setdefault(node.parent_id, []).append(node)
        for values in children.values():
            values.sort(key=lambda item: item.sequence)

        visiting: set[str] = set()
        visited: set[str] = set()

        def build(node: RequirementRuleNode) -> ConditionNode:
            if node.id in visiting:
                raise ValueError("Requirement rule tree contains a cycle")
            if node.id in visited:
                raise ValueError("Requirement rule tree reuses a node")
            visiting.add(node.id)
            child_nodes = [build(child) for child in children.get(node.id, [])]
            visiting.remove(node.id)
            visited.add(node.id)

            if node.node_type == RequirementRuleNodeType.CONDITION:
                if node.field is None or node.operator is None:
                    raise ValueError("Condition node is missing field or operator")
                if child_nodes:
                    raise ValueError("Condition node cannot have children")
                from packages.domain.requirement.conditions import RequirementConditionCandidate
                return ConditionLeaf(
                    RequirementConditionCandidate(
                        requirement_id,
                        node.field,
                        node.operator,
                        node.value,
                    )
                )

            if node.group_operator is None:
                raise ValueError("Group node is missing an operator")
            if node.group_operator.value == "NOT" and len(child_nodes) != 1:
                raise ValueError("NOT group requires exactly one child")
            if node.group_operator.value in {"AND", "OR"} and not child_nodes:
                raise ValueError("AND/OR group requires at least one child")
            return ConditionGroup(node.group_operator, tuple(child_nodes))

        result = build(roots[0])
        if len(visited) != len(nodes):
            raise ValueError("Requirement rule tree contains unreachable nodes")
        return result
