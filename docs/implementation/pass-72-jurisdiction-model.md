# Pass 72 — Jurisdiction Model

A jurisdiction is now a governed hierarchical concept rather than a free-form label.

Each jurisdiction has a stable identifier, name, type, optional code, optional parent and active status.

Supported types:

- GLOBAL
- REGIONAL
- COUNTRY
- TERRITORY
- CUSTOM

This permits Global -> ECOWAS -> Nigeria, while also allowing AfCFTA or other regional/international regimes to exist as independent jurisdiction nodes.

The existing country master data remains the scenario/product country reference. The jurisdiction registry is the compliance-authority scope model and is intentionally not conflated with country data.

MOUs can therefore be scoped to a jurisdiction while their signing parties remain separate metadata.
