# Pass 147 — Conservative short-circuit on the canonical path

## Objective

Carry the earlier conservative evaluation-read optimization onto the now-canonical revision-aware service.

## Implemented

- After materializing the exact rule-set revision, evaluation checks temporal effectiveness and scope.
- If the revision is definitely inactive on the scenario date, or scope is definitively `False`, evidence and rule-node repositories are not queried.
- The deterministic evaluator still runs and persists the result and trace, so the requirement is represented as not applicable rather than silently omitted.
- Unknown scope does not trigger the short-circuit. Such requirements continue through evidence and revision-bound rule-tree loading so the evaluator can preserve an unresolved outcome when appropriate.
- A regression test verifies that an expired revision produces a persisted `NOT_APPLICABLE` result and trace without touching evidence or rule-node repositories.

## Guardrails

This is a read optimization, not a rule-selection filter. It does not remove memberships from the active rule set, change temporal/scope semantics, or infer legal effect from document-version relationships.

## Verification status

Review the latest GitHub Actions runs. The repository's Ruff stage has a large existing backlog and currently stops CI before type checking and tests; a failed lint stage must not be reported as a test failure or a green test run.

## Next

Continue auditing rule-set publication and activation so invalid revisions, malformed rule trees, and missing catalog references are rejected before a rule set becomes active.
