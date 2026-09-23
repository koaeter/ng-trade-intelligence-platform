# Pass 88 — Acquisition history application query

A small application query now exposes acquisition history through the application layer instead of requiring callers to depend directly on SQLAlchemy repositories. The query remains read-only and preserves newest-first ordering supplied by the persistence adapter.
