Pass 106 — Re-extraction & Change Detection

Pass 106 introduces deterministic comparison of immutable extraction runs.

## Rules

- Runs must belong to the same source artifact.
- A run cannot be compared with itself.
- Input SHA-256 is compared first.
- Segment text is ordered deterministically and hashed without rewriting the text.
- SAME_INPUT_SAME_OUTPUT means identical input bytes and extracted segment text.
- SAME_INPUT_DIFFERENT_OUTPUT means identical input bytes but different extraction output.
- DIFFERENT_INPUT_DIFFERENT_OUTPUT means input bytes changed and extraction output changed.

A processing difference is not a legal conclusion and does not prove that a document was amended. Extractor identity/version remains on each immutable run for later analysis.

Comparisons are append-only and do not overwrite source artifacts or extraction runs.

## Next layer

Segment-level document/extraction diffing can identify additions, removals, and modifications while retaining exact source locations.