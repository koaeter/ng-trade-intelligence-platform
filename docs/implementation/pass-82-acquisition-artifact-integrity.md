# Pass 82 — Acquisition-to-artifact integrity

A successful acquisition event can be linked to a captured artifact only when three invariants hold:

1. the event exists and belongs to the same source;
2. the event completed successfully;
3. the event response SHA-256 equals the persisted artifact SHA-256.

This makes the acquisition event an auditable claim about the exact bytes that became the stored artifact. Failed or cross-source events cannot be used as artifact provenance.
