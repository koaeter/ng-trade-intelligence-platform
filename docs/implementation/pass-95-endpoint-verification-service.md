# Pass 95 — Authority endpoint verification service

Endpoint verification is now an application operation. It probes the configured endpoint through the existing bounded source fetcher and records VERIFIED or FAILED status, timestamp, and a bounded failure note.

Verification is operational only: it confirms reachability through the configured acquisition boundary and does not establish legal authority or publish regulatory knowledge.
