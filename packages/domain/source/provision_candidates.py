from dataclasses import dataclass
from enum import Enum


class ProvisionCandidateStatus(str, Enum):
    EXTRACTED = "EXTRACTED"
    REVIEWED = "REVIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class ProvisionCandidate:
    id: str
    document_id: str
    artifact_id: str
    extraction_segment_id: str
    text: str
    locator: str
    candidate_type: str = "UNCLASSIFIED"
    status: ProvisionCandidateStatus = ProvisionCandidateStatus.EXTRACTED
