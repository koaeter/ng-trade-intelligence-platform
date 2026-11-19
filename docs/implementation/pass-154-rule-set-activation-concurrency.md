# Pass 154 — Rule-set activation concurrency verification

## Change

Added a PostgreSQL integration test that starts two independent sessions at the same time and attempts to activate two different PUBLISHED rule-set versions while one existing version is ACTIVE.

The test asserts that:

- One or both competing activations may commit, depending on transaction serialization. If both commit, the later serialized activation replaces the earlier one.
- If the database rejects a competing activation, the losing transaction receives an integrity conflict.
- Exactly one rule set remains ACTIVE after both transactions finish.
- The winner is one of the two requested target versions.

The repository activation implementation now retires and flushes the previous ACTIVE version before setting the replacement ACTIVE. This avoids transient violations of the partial unique index on databases that apply immediate unique checks to a flush batch. Both steps remain inside the caller's transaction, so rollback restores the previous state if the second step fails.

## Invariant

The application-level lock strategy is an optimisation and coordination mechanism. The database partial unique index remains the final authority enforcing at most one ACTIVE rule set.

## Verification boundary

This test requires the PostgreSQL service configured by CI and is marked as an integration test. A passing test demonstrates the tested concurrent activation scenario; it does not replace production database isolation review or operational monitoring.


## Verification result

The PostgreSQL integration concurrency test passed in CI. The full suite reported **257 passed** on the verified baseline before the subsequent audit-constraint and Keycloak-token hardening changes; those changes have also passed the staged CI gate.
