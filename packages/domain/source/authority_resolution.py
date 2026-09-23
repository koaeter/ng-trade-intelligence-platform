from dataclasses import dataclass
from datetime import date
from packages.domain.source.authority import SourceAuthorityAssignment


@dataclass(frozen=True)
class AuthorityResolution:
    selected: SourceAuthorityAssignment | None
    candidates: tuple[SourceAuthorityAssignment, ...]
    status: str
    reason: str


def resolve_authority(assignments: list[SourceAuthorityAssignment], as_of: date) -> AuthorityResolution:
    active = [
        item for item in assignments
        if (item.effective_from is None or item.effective_from <= as_of)
        and (item.effective_to is None or as_of <= item.effective_to)
        and item.verification_status == "VERIFIED"
    ]
    if not active:
        return AuthorityResolution(None, (), "UNRESOLVED", "No verified authority assignment is effective for the requested date.")
    ordered = sorted(active, key=lambda item: (item.precedence, -item.legal_weight, item.id))
    best = ordered[0]
    tied = [item for item in ordered if (item.precedence, item.legal_weight) == (best.precedence, best.legal_weight)]
    if len(tied) > 1:
        return AuthorityResolution(None, tuple(ordered), "CONFLICT", "Multiple verified assignments have identical precedence and legal weight.")
    return AuthorityResolution(best, tuple(ordered), "RESOLVED", "Selected the highest-precedence verified assignment effective on the requested date.")
