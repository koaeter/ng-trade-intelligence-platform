# Pass 136 — Dual-Mode Provenance API

Document provenance now supports two complementary read modes.

- **Summary mode** provides count-only metadata for lightweight navigation.
- **Expanded mode** remains available through the existing provenance endpoint.
- Dedicated detail endpoints remain available for drilling into individual collections.

The summary is a read-only projection and does not infer legal effect, supersession, amendment, repeal, applicability, or compliance conclusions from provenance records.
