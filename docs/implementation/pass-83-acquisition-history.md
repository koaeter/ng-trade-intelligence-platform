# Pass 83 — Acquisition history and persistence

The acquisition-event persistence boundary is now complete. SQLAlchemy can create, retrieve, link, and list acquisition events per source. Source artifacts persist their acquisition-event reference. Events are ordered newest-first so failed and successful attempts remain visible as an auditable retrieval history.
