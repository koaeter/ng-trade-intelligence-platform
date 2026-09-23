# Pass 84 — Registered-source acquisition orchestration

Acquisition can now be initiated by source ID rather than by passing an arbitrary URL into the workflow. The orchestration service loads the registered source, requires an authority-endpoint link and registered acquisition URL, and delegates to tracked acquisition. This closes the application boundary between source registration and retrieval.
