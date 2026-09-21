# Pass 21 — Master Data Persistence Boundary

Product, HS Version, HS Code, Country, and Market now have PostgreSQL persistence models and repository implementations.

HS classification is versioned by `(HS version, code)`, preventing an HS code from being treated as timeless.

Export scenarios will progressively use these governed references rather than free-form identifiers.

Master data is authoritative domain data; search, graph, embeddings, and AI representations remain derived projections.

Next: Pass 22 — master-data seeding and validation, followed by real source/regulatory data integration.
