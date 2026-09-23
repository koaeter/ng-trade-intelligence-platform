from packages.application.source.authority_scope_seed import INITIAL_NIGERIAN_AUTHORITY_SCOPES
from packages.domain.source.authority_scope import AuthorityScopeAssignment


def test_scope_assignment_is_not_a_precedence_decision():
    assignment = AuthorityScopeAssignment("x", "naqs", "ng", "sps", "CERTIFICATION")
    assert assignment.authority_id == "naqs"
    assert assignment.regulatory_domain_code == "sps"
    assert assignment.fact_type_code == "CERTIFICATION"


def test_nigerian_scope_seed_has_no_duplicate_scope_keys():
    keys = [
        (x.authority_id, x.jurisdiction_id, x.regulatory_domain_code, x.fact_type_code)
        for x in INITIAL_NIGERIAN_AUTHORITY_SCOPES
    ]
    assert len(keys) == len(set(keys))


def test_scope_seed_covers_core_nigerian_competent_authorities():
    authorities = {x.authority_id for x in INITIAL_NIGERIAN_AUTHORITY_SCOPES}
    assert {"nepc", "ncs", "son", "nafdac", "naqs", "dvcps", "fisheries", "ninas"} <= authorities
