# Pass 57 — Revision-aware evaluation

## Objective

Make historical evaluation use the active rule-set's immutable requirement revisions rather than the mutable current Requirement rows.

## Implemented

RevisionAwareEvaluationService now:
- resolves the active rule-set version
- resolves its requirement memberships
- loads the exact requirement revision
- materializes the revision into evaluation context
- loads rule nodes bound to that revision
- evaluates temporal validity, scope, conditions and evidence
- persists the result and trace using the active rule-set version

## Result

The evaluation path is now:

Scenario
  -> Active Rule Set
  -> Requirement Membership
  -> Immutable Requirement Revision
  -> Revision-bound Rule Tree
  -> Deterministic Evaluation
  -> Trace

## Next

The next pass should add rule-set publication validation so an active rule-set cannot be activated while it contains missing revisions, invalid rule trees or unresolvable reference data.
