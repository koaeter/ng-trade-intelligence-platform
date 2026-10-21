# Pass 150 — Atomic activation and authorization contract

## Implemented

- Added a PostgreSQL partial unique index restricting the database to at most one `ACTIVE` rule-set version (migration `0037`). The SQLAlchemy model mirrors the partial predicate for SQLite-based tests.
- Added a repository activation operation that locks the target row, verifies it is still published or active, locks existing active rows, retires the previous active version, and activates the target within the caller's transaction.
- Updated the application service to require that atomic repository operation rather than performing separate status updates.
- Added repository-level tests for transactional status switching and rejection of two active versions.
- Added a framework-independent authorization policy that accepts a principal only after an authentication adapter has validated identity and permissions. It rejects missing identities and missing permissions.
- Added tests for the authorization policy and strengthened draft authoring to reject duplicate revision IDs and multiple revisions for one requirement before writing.

## Security boundary

The administrative HTTP write endpoints remain intentionally unexposed. The repository does not yet have a configured identity provider or token-validation adapter. The authorization policy is not itself authentication and must not be treated as proof of identity. An OIDC/OAuth2 provider and its issuer/audience/signature/expiry validation still need to be configured before protected endpoints can be wired.

## Verification status

The existing CI workflow runs Ruff before type checking and tests. Ruff reports hundreds of repository-wide violations and exits early, which skips those later steps. Recent runs have not yet verified the new tests. Some lint issues in touched files have been corrected, but the broader lint backlog remains.

## Next

- Continue reducing lint violations in the touched paths without hiding the repository-wide backlog.
- Verify the activation and authorization tests in CI.
- Add immutable audit records for successful administrative lifecycle transitions.
- Before exposing the administrative API, choose the identity provider and integrate its validated claims with the permission policy.
