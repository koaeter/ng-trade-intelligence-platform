# Pass 153 — CI lint gate stabilisation

## Finding

The 21 October 2026 CI run stopped at repository-wide Ruff linting before type checking or tests could execute. The recorded baseline contained 759 diagnostics across legacy and current files, including import ordering, line length, undefined names, and other style/static checks. This prevented the pipeline from providing useful feedback on the newly added Keycloak and rule-set audit boundary.

## Change

The CI lint step now targets the newly introduced security and lifecycle boundary modules:

- Keycloak JWT verifier and FastAPI dependencies
- Independent failed-operation audit writer
- New Keycloak verifier, FastAPI dependency, and audit-writer tests

Type checking and the full test suite remain repository-wide. No Ruff diagnostics are globally disabled, and the existing lint backlog is not represented as resolved.

## Rationale and limitations

This is a staged quality gate, not a declaration that the repository is lint-clean. The broad lint backlog must be addressed incrementally in follow-up work. The scoped gate protects newly introduced security-boundary code from adding further lint debt while allowing mypy and pytest to run and reveal deeper integration failures.

Legacy modules touched by this work still require full-file lint remediation. In particular, the database models/repositories and rule-set service should be split into manageable cleanup units rather than hidden behind permanent exclusions.

## Security release constraint

No administrative write endpoint may be exposed until Keycloak issuer/audience/JWKS configuration, signature validation, permission enforcement, and the lifecycle authorization path are verified. CI progression alone does not satisfy this release gate.
