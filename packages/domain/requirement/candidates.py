from dataclasses import dataclass
from enum import Enum


class RequirementCandidateStatus(str, Enum):
    EXTRACTED = "EXTRACTED"
    REVIEWED = "REVIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class RequirementCandidate:
    id: str
    provision_id: str
    document_id: str
    proposed_name: str
    text: str
    status: RequirementCandidateStatus = RequirementCandidateStatus.EXTRACTED
