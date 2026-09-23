# Pass 60 — Rule-set lifecycle governance

## Objective

Replace direct ACTIVE/RETIRED transitions with an explicit publication lifecycle.

## Lifecycle

DRAFT
  -> VALIDATED
  -> PUBLISHED
  -> ACTIVE
  -> RETIRED

The active version can be replaced by a newly published version, after which the previous active version becomes retired.

## Implemented

- Added DRAFT, VALIDATED and PUBLISHED states.
- Validation requires the rule-set validator.
- Publication requires VALIDATED state.
- Activation requires PUBLISHED or existing ACTIVE state.
- Activation still validates the target before switching active state.

## Governance effect

The platform now has a distinct point where a rule-set has passed structural validation but has not yet been made active.

## Next

The next pass should build the rule-set authoring/publishing application boundary, including creation of revisions and membership from reviewed requirements.
