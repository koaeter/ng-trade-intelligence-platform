# Pass 71 — Source Authority Matrix and Instrument Model

## Purpose

Establish the authority model needed to distinguish an official source from the legal or administrative effect of a particular instrument.

## Source authority matrix

Authority is not represented by one global source ranking. A source receives an authority assignment scoped to jurisdiction, regulatory domain, fact type and temporal validity.

The assignment records authority type, deterministic precedence, legal weight, verification status and supersession. This permits one institution to have different authority for different facts.

## Instrument model

Documents may be classified as instruments through a separate Instrument record. Instrument type is distinct from legal effect.

Supported types include laws, regulations, treaties, trade agreements, MOUs, MOAs, tariff schedules, notices, circulars, guidelines, standards, procedures and administrative decisions.

Supported legal effects distinguish binding, conditionally binding, administrative, cooperative, reference, informative and unknown.

## MOU treatment

An MOU is a first-class instrument attached to its source document. The system does not infer that an MOU is legally binding merely because it was issued or signed by an official authority.

An MOU can contain provisions that become inputs to the existing pipeline:

MOU document -> provision -> reviewed provision -> requirement/rule

The resulting requirement retains the MOU as its evidence and preserves the instrument and legal-effect metadata.

The MOU model also records parties and supersession so later passes can model amendments, annexes, termination and replacement without losing provenance.

## Deliberate deferrals

Jurisdictions, regulatory domains and fact types are currently controlled strings. Dedicated registries and hierarchical relationships are deferred to following passes.
