# Pass 85 — Artifact linkage atomicity boundary

Acquisition-event validation now happens before the artifact repository write. A missing, failed, cross-source, or checksum-mismatched acquisition event cannot leave behind a persisted artifact that claims invalid provenance.

The sequence is now: validate acquisition provenance -> persist artifact -> link event to artifact -> advance source lifecycle.
