# Pass 67 — Acquisition lifecycle integration

## Objective

Connect successful artifact acquisition to the governed Source lifecycle.

## Implemented

When a discovered source successfully produces an acquired artifact, the source transitions to ACQUIRED.

Acquisition failure does not advance the source lifecycle.

The source repository now has an explicit update boundary rather than requiring callers to replace status records directly.

## Next

The next pass should connect extraction completion and candidate creation to EXTRACTED/CANDIDATE lifecycle states.
