from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorityScopeAssignment:
    """Declares the regulatory knowledge scope an authority may cover.

    This is a scope registry, not a legal-precedence decision. Precedence remains
    fact/domain/jurisdiction/time specific and is resolved through source
    authority assignments when an actual source is evaluated.
    """

    id: str
    authority_id: str
    jurisdiction_id: str
    regulatory_domain_code: str
    fact_type_code: str
    active: bool = True
    notes: str | None = None
