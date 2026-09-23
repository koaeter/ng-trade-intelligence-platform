from dataclasses import dataclass

from packages.domain.requirement.candidates import RequirementCandidate
from packages.domain.source.models import Provision


@dataclass(frozen=True)
class RequirementCandidateExtractor:
    """Creates reviewable requirement candidates from accepted provisions.

    It does not infer applicability scope or create an authoritative Requirement.
    """

    def extract(self, provisions: list[Provision]) -> list[RequirementCandidate]:
        candidates = []
        for provision in provisions:
            text = " ".join(provision.text.split())
            if not text:
                continue
            candidates.append(
                RequirementCandidate(
                    id=f"{provision.id}:requirement-candidate",
                    provision_id=provision.id,
                    document_id=provision.document_id,
                    proposed_name=self._proposed_name(text),
                    text=text,
                )
            )
        return candidates

    @staticmethod
    def _proposed_name(text: str) -> str:
        words = text.split()
        return " ".join(words[:12]).rstrip(".,:;") or "Unnamed requirement candidate"
