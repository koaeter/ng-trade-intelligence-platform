from packages.application.source.regulatory_document_seed import INITIAL_NIGERIAN_DOCUMENTS


def test_initial_documents_reference_registered_sources():
    assert len(INITIAL_NIGERIAN_DOCUMENTS) >= 5
    assert all(document.source_id for document in INITIAL_NIGERIAN_DOCUMENTS)


def test_nafdac_documents_preserve_explicit_effective_dates():
    by_id = {x.id: x for x in INITIAL_NIGERIAN_DOCUMENTS}
    assert by_id["doc-nafdac-export-e-license"].effective_from.isoformat() == "2022-09-24"
    assert by_id["doc-nafdac-export-e-license"].effective_to.isoformat() == "2027-09-23"
