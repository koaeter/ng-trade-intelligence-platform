# Pass 145 — Canonical revision-aware evaluation

## Objective

Make the API's production evaluation endpoint use immutable requirement revisions selected by the active rule set, while retaining the legacy evaluation implementation until its remaining callers and compatibility needs are audited.

## Implemented

- The export-scenario evaluation endpoint now constructs and invokes `RevisionAwareEvaluationService`.
- The service resolves the active rule-set version and evaluates only the requirement revisions listed in that rule set's memberships.
- Rule nodes are loaded with `list_for_revision(revision.id)`, preventing nodes from another revision of the same requirement from entering the tree.
- Evaluation results and deterministic traces are persisted with the active rule-set version.
- A missing scenario remains a not-found response. A missing active rule set is reported as a conflict because evaluation cannot safely proceed without a published evaluation scope.
- The legacy `evaluate_scenario` function remains available for controlled migration and compatibility; the API endpoint no longer calls it.
- The revision-aware unit test now fails if the service tries to load rule nodes by requirement ID instead of revision ID.

## Guardrails

- Rule-set membership defines the evaluation scope; unlisted legacy requirements are not implicitly evaluated.
- A requirement revision is not silently substituted with the latest revision.
- Rule-node loading remains revision-bound, and the rule-tree loader continues validating node ownership.
- Evidence and trace persistence remain part of the same request transaction, committed only after evaluation succeeds.

## Verification status

GitHub Actions should be checked for the commits in this pass before describing the change as CI-green. The repository has previously had a large pre-existing Ruff backlog, so lint failures must be distinguished from evaluation or API test failures.

## Next

Audit publication validation and the API integration path. In particular, verify that active rule sets cannot be published with missing revisions, invalid revision-bound rule trees, or unresolvable catalog references. Keep the legacy path isolated until its remaining use cases are understood.
