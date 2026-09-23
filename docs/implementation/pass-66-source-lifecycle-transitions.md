# Pass 66 — Source lifecycle transitions

## Objective

Turn source lifecycle states into explicit transition rules rather than arbitrary status updates.

## Implemented

Allowed lifecycle progression now includes:

DISCOVERED
  -> ACQUIRED
  -> EXTRACTED
  -> CANDIDATE
  -> REVIEWED
  -> PUBLISHED
  -> SUPERSEDED
  -> RETIRED

Reprocessing can return REVIEWED material to CANDIDATE, while invalid transitions are rejected.

## Important distinction

Source lifecycle status describes the governance/processing state of source knowledge. It does not mean that every artifact inside a source has the same processing state.

## Next

The next pass should connect acquisition, extraction and candidate publication services to these lifecycle transitions without allowing a downstream stage to skip governance.
