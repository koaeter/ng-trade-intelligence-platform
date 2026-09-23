# Pass 37 — Controlled provision types

## Objective

Prevent accepted regulatory provisions from carrying arbitrary semantic labels.

## Implemented

Added a controlled ProvisionType vocabulary covering:
- requirement
- prohibition
- definition
- procedure
- eligibility condition
- exception
- tariff rule
- origin rule
- licensing rule
- document requirement
- penalty
- scope
- reference
- other

The review boundary now validates accepted provision types against this vocabulary.

## Governance effect

An extracted sentence can remain an UNCLASSIFIED candidate. A human review decision must explicitly select a supported provision type before the system creates a Provision.

This is deliberately a classification boundary, not an attempt to infer legal meaning automatically.

## Next

The next pass should make provision-to-evidence provenance a first-class query path and prepare the structure required for deriving governed Requirement candidates from accepted provisions.
