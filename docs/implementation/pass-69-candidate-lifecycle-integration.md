# Pass 69 — Candidate lifecycle integration

## Objective

Advance source governance to CANDIDATE when extraction has produced reviewable provision candidates.

## Implemented

ProvisionCandidateExtractor can now update the source lifecycle after creating one or more candidates.

No lifecycle advancement occurs for an empty extraction result.

## Governance boundary

CANDIDATE means extracted material exists that requires review. It does not mean the candidate is legally accepted.

## Next

The next pass should connect accepted/rejected provision review outcomes to REVIEWED source state while preserving review history.
