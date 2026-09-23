from datetime import date

from packages.domain.source.authority import (
    AuthorityType, Instrument, InstrumentType, LegalEffect, SourceAuthorityAssignment,
)


def test_authority_assignment_is_scoped_to_fact_and_jurisdiction():
    assignment = SourceAuthorityAssignment(
        id="a1", source_id="ncs-tariff", authority_type=AuthorityType.PRIMARY_LEGAL,
        jurisdiction="NG", domain="CUSTOMS", fact_type="TARIFF", precedence=10,
        legal_weight=100, effective_from=date(2026, 1, 1),
    )
    assert assignment.jurisdiction == "NG"
    assert assignment.domain == "CUSTOMS"
    assert assignment.fact_type == "TARIFF"


def test_mou_is_an_instrument_with_distinct_legal_effect():
    instrument = Instrument(
        id="mou-1", document_id="doc-1", instrument_type=InstrumentType.MOU,
        legal_effect=LegalEffect.COOPERATIVE,
        parties=("NEPC", "DESTINATION_AUTHORITY"),
    )
    assert instrument.instrument_type is InstrumentType.MOU
    assert instrument.legal_effect is LegalEffect.COOPERATIVE
    assert instrument.parties == ("NEPC", "DESTINATION_AUTHORITY")


def test_mou_does_not_imply_binding_effect():
    instrument = Instrument(
        id="mou-2", document_id="doc-2", instrument_type=InstrumentType.MOU,
        legal_effect=LegalEffect.UNKNOWN,
    )
    assert instrument.legal_effect is LegalEffect.UNKNOWN


def test_precedence_is_explicit():
    assignment = SourceAuthorityAssignment(
        id="a2", source_id="source-2",
        authority_type=AuthorityType.OFFICIAL_ADMINISTRATIVE,
        jurisdiction="NG", domain="SPS", fact_type="CERTIFICATION",
        precedence=20, legal_weight=70,
    )
    assert assignment.precedence > 0
