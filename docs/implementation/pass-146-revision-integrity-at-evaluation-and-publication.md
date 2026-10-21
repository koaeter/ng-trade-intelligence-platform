# Pass 146 — Revision integrity at evaluation and publication

## Objective

Apply the same revision-integrity rules at both rule-set publication and runtime evaluation.

## Implemented

- Runtime evaluation rejects a membership whose `requirement_id` disagrees with the referenced immutable revision's `requirement_id`.
- Rule-set publication validation now loads rule nodes by the exact revision ID rather than by requirement ID.
- Publication and runtime therefore inspect the same revision-scoped rule tree. Nodes from older or newer revisions cannot accidentally be mixed into validation or evaluation.
- Unit tests assert that publication validation and runtime evaluation do not fall back to requirement-wide node lookup.
- Added a negative test for a rule-set membership that points to a revision belonging to a different requirement.

## Why this matters

A rule set is a versioned, reviewable scope of requirements. If a membership references a revision belonging to another requirement, the platform must reject it rather than silently evaluate a different requirement. Likewise, validation must inspect the exact rule tree that runtime will evaluate.

## Verification status

Check GitHub Actions before treating this pass as green. The existing repository-wide Ruff backlog currently causes CI to stop before type checking and tests, so lint status alone does not establish whether these tests pass.

## Next

Audit the active-rule-set selection and publication lifecycle, then move the conservative evidence-loading short-circuit from the legacy evaluation path into the revision-aware path without skipping any requirement that could still apply.
