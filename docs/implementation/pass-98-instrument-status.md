# Pass 98 — Controlled instrument lifecycle status

Instrument status is now a controlled domain value rather than an unconstrained string:

- DRAFT
- ACTIVE
- SUPERSEDED
- TERMINATED
- EXPIRED

This applies equally to laws, agreements, MOUs, MOAs, notices, standards, and other instrument types. Legal effect remains a separate field, so an MOU's lifecycle status cannot be mistaken for a statement about its legal force.
