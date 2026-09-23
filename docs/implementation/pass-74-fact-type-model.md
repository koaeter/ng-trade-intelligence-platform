# Pass 74 — Fact Type Model

Fact types are now governed entities. They describe the kind of claim a source is authoritative for, independently of the source and instrument.

Examples include:

- TARIFF
- PREFERENTIAL_TARIFF
- RULES_OF_ORIGIN
- PROHIBITION
- RESTRICTION
- LICENCE
- CERTIFICATION
- STANDARD
- SPS_MEASURE
- TBT_MEASURE
- DOCUMENTATION
- PROCEDURE
- TRADE_REMEDY
- QUOTA
- MARKET_ACCESS

The registry is deliberately data-driven. This prevents the authority matrix from encoding these concepts as uncontrolled strings while still allowing new fact types without changing application code.
