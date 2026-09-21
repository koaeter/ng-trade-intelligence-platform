# Pass 20 — Governed Product, HS, Country & Market Concepts

## Goal

Replace raw scenario strings with governed domain concepts while preserving the separation between domain models and persistence.

## Implemented

The domain now has first-class:

- Product
- HSCode
- Country
- Market

Application repository ports have also been introduced for these concepts.

These objects are intentionally small. They establish identity and ownership boundaries without prematurely implementing classification mappings, country hierarchies, market jurisdictions, or external master-data ingestion.

## Why this matters

The export scenario is ultimately evaluated against governed references:

Product + HS classification + origin country + destination market + date.

This allows later passes to enforce:

- versioned HS classifications
- product-to-HS mappings
- country/jurisdiction relationships
- market-specific requirements
- historical validity

## Next

Pass 21 will introduce the first governed persistence/master-data slice and connect these entities to export scenarios.
