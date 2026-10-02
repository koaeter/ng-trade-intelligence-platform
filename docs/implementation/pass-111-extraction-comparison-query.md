# Pass 111 — Extraction Comparison Query Surface

## Goal

Provide a dedicated application read contract for immutable extraction comparisons before exposing comparison metadata through the API.

## Contract

GetExtractionComparison loads one ExtractionComparison by ID and rejects missing comparisons with a domain-independent ValueError.

The query is read-only and does not recompute hashes, compare segments, or modify extraction state.

## Governance boundary

An extraction comparison describes deterministic processing lineage between two extraction runs. It does not establish that a difference is legally meaningful, represents an amendment, or changes an export-compliance requirement.

## Tests

Coverage verifies successful retrieval and missing-comparison rejection.
