# Pass 86 — Ingestion failure cleanup

Source ingestion now treats the stored object as provisional until provenance validation, artifact persistence, event linkage, and source lifecycle advancement complete locally. If the ingestion operation fails after object storage succeeds, the newly stored object is deleted on a best-effort basis so failed ingestion does not routinely leave orphaned artifacts.

A database transaction remains the authoritative boundary for durable metadata commits; deployment should commit the repository changes and object-storage lifecycle together through an application unit-of-work/outbox strategy as the platform moves to production.
