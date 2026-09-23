from dataclasses import dataclass

from packages.domain.source.extraction import ExtractionSegment
from packages.domain.source.provision_candidates import ProvisionCandidate


@dataclass(frozen=True)
class ProvisionCandidateExtractor:
    """Turns bounded extraction segments into reviewable candidates.

    This stage deliberately does not decide that a fragment is legally authoritative.
    Classification and publication remain separate governance steps.
    """

    def extract(
        self,
        document_id: str,
        segments: list[ExtractionSegment],
    ) -> list[ProvisionCandidate]:
        candidates: list[ProvisionCandidate] = []
        for segment in segments:
            text = " ".join(segment.text.split())
            if not text:
                continue
            locator = segment.locator or self._fallback_locator(segment)
            candidates.append(
                ProvisionCandidate(
                    id=f"{document_id}:candidate:{segment.sequence}",
                    document_id=document_id,
                    artifact_id=segment.artifact_id,
                    extraction_segment_id=segment.id,
                    text=text,
                    locator=locator,
                )
            )
        return candidates

    @staticmethod
    def _fallback_locator(segment: ExtractionSegment) -> str:
        if segment.page_number is not None:
            return f"page={segment.page_number};sequence={segment.sequence}"
        return f"sequence={segment.sequence}"
