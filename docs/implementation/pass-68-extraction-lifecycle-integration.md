# Pass 68 — Extraction lifecycle integration

## Objective

Advance a source from ACQUIRED to EXTRACTED only after successful bounded document extraction.

## Implemented

ExtractedTextService can now update the governed source lifecycle after a successful extraction.

Extraction failures do not advance the source state.

The artifact remains independently tracked with its own processing metadata.

## Next

The next pass should connect provision-candidate creation to the CANDIDATE lifecycle state while keeping candidate extraction non-authoritative.
