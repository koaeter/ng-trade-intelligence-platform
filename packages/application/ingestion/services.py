from packages.application.scenarios.repositories import EvidenceRepository, RequirementRepository
from packages.application.source.repositories import DocumentRepository, ProvisionRepository, SourceRepository
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.source.models import Document, Provision, Source, SourceStatus


class RegulatoryKnowledgeIngestionService:
    """Small orchestration boundary for source-to-knowledge publication.

    Extraction/AI may propose candidates, but publication requires verified evidence.
    """

    def __init__(
        self,
        sources: SourceRepository,
        documents: DocumentRepository,
        provisions: ProvisionRepository,
        evidence: EvidenceRepository,
        requirements: RequirementRepository,
    ) -> None:
        self.sources = sources
        self.documents = documents
        self.provisions = provisions
        self.evidence = evidence
        self.requirements = requirements

    def publish_requirement(
        self,
        source: Source,
        document: Document,
        provision: Provision,
        evidence: Evidence,
        requirement: Requirement,
    ) -> Requirement:
        if source.status not in {SourceStatus.REVIEWED, SourceStatus.PUBLISHED}:
            raise ValueError("Source must be reviewed before knowledge can be published")
        if document.source_id != source.id:
            raise ValueError("Document does not belong to source")
        if provision.document_id != document.id:
            raise ValueError("Provision does not belong to document")
        if evidence.source_id != source.id:
            raise ValueError("Evidence does not belong to source")
        if evidence.document_id != document.id or evidence.provision_id != provision.id:
            raise ValueError("Evidence must point to the document and provision")
        if not evidence.verified:
            raise ValueError("Unverified evidence cannot support published knowledge")
        if evidence.id not in requirement.evidence_ids:
            raise ValueError("Requirement must reference its supporting evidence")
        self.sources.add(source)
        self.documents.add(document)
        self.provisions.add(provision)
        self.evidence.add(evidence)
        self.requirements.add(requirement)
        return requirement
