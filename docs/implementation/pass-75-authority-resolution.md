# Pass 75 — Deterministic Authority Resolution

Authority resolution is now explicit and explainable.

For a requested date, the resolver:
1. filters assignments by temporal validity;
2. excludes unverified assignments;
3. orders candidates by deterministic precedence;
4. uses legal weight as the secondary discriminator;
5. returns a conflict rather than silently choosing when candidates remain tied.

The resolver returns the complete ordered candidate set so a later evaluation trace can explain why a source was selected.

This is a resolution mechanism, not a legal opinion. A conflict that cannot be deterministically resolved remains CONFLICT and must be surfaced for review.
