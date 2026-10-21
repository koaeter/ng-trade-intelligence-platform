# Pass 143 — Conservative Evaluation Read Short-Circuit

## Goal

Reduce avoidable evidence and rule-node repository reads during scenario evaluation without truncating the requirement set or changing applicability semantics.

## Changes

- The orchestrator checks requirement temporal validity and explicit scope mismatch before loading evidence or rule nodes.
- Requirements outside their effective period or explicitly outside scenario scope still receive a normal deterministic evaluation and persisted trace.
- Requirements with unknown or incomplete scope are **not** excluded. They continue through rule/evidence loading and the standard evaluator.
- Added a regression test asserting that expired requirements produce `NOT_APPLICABLE` while evidence and rule repositories are not accessed.

## Safety boundary

This is a conservative read optimization, not a candidate-index implementation. The orchestrator still enumerates all requirements and emits one result and trace per requirement. It does not cap or silently omit requirements, infer legal effects, or treat missing scope information as a mismatch.

## Verification

The targeted unit test was added, but this pass should not be described as CI-verified until the corresponding workflow result is inspected. Repository-wide Ruff failures have previously existed independently of this change.
