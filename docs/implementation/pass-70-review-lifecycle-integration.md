# Pass 70 — Review lifecycle integration

## Objective

Advance a source to REVIEWED only when its provision candidates have all reached terminal review outcomes.

## Implemented

ProvisionReviewService can now:
- retain review history
- accept or reject individual candidates
- inspect all candidates for the document
- transition the source from CANDIDATE to REVIEWED only when every candidate is ACCEPTED or REJECTED

A partially reviewed document remains in CANDIDATE.

## Governance effect

The source cannot be marked reviewed simply because one candidate was reviewed.

## Next

The next pass should connect accepted reviewed knowledge to PUBLISHED source status through the existing publication governance boundary.
