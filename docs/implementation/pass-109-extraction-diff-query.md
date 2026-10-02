# Pass 109 — Extraction-Diff Query Surface

Pass 109 adds the application read boundary for persisted extraction diffs.

## Read operations

- `GetExtractionDiff`: retrieves one immutable diff and returns its entries ordered by ordinal.
- `ListExtractionDiffs`: scopes persisted diffs to an `ExtractionComparison`.

Neither operation recomputes the diff or mutates extraction lineage.

## Integrity boundary

The query layer deliberately returns the processing evidence already persisted. It does not transform entry types into legal conclusions or compliance decisions.

## Next boundary

The next pass can address API/read-model exposure after the application query contract is established and tested.