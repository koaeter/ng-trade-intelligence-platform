# Pass 96 — Endpoint verification API

A verification endpoint now runs the bounded HTTPS probe for a registered authority endpoint and persists its operational verification result. The probe's allowlist is restricted to the hostname already stored in the endpoint registry; the registry remains the trust boundary for which endpoint may be probed.
