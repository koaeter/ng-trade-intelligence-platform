# Pass 56 — Bind rule nodes to requirement revisions

## Objective

Ensure a persisted condition tree belongs to a specific immutable requirement revision.

## Implemented

RequirementRuleNode now carries requirement_revision_id.

The loader validates both:
- logical requirement identity
- immutable requirement revision identity

The database links rule nodes directly to requirement_revisions.

## Historical evaluation boundary

RuleSet
  -> RequirementRevision
  -> RuleNodes
  -> ConditionTree
  -> Evaluation

A current requirement edit can therefore not silently change the rule tree used by an older revision.

## Migration note

The migration deliberately treats existing unbound rule nodes as non-authoritative and requires them to be assigned a revision before evaluation. No historical rule nodes should be silently guessed.

## Next

The next pass should update rule-tree creation/persistence to require a revision and add a complete revision-aware evaluation loader.
