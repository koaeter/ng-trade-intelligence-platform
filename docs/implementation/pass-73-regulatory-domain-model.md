# Pass 73 — Regulatory Domain Model

Regulatory domains are now governed entities rather than arbitrary strings.

The registry supports hierarchical domains, for example:

Trade
  - Customs
  - Tariffs
  - Rules of Origin
  - Trade Remedies

Product Regulation
  - Standards / Conformity
  - SPS
  - TBT
  - Licensing

Documentation and Procedures can also be represented as domains.

The hierarchy is intentionally data-driven. The initial registry is not populated with legal classifications in this pass; later source-registry passes can establish the controlled vocabulary.
