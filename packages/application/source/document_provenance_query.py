from dataclasses import dataclass

from packages.application.source.artifact_repositories import SourceArtifactRepository
from packages.application.source.extraction_repositories import (
    ExtractionRunRepository,
    ExtractionSegmentRepository,
)
from packages.application.source.document_version_repositories import (
    DocumentVersionRepository,
)
from packages.application.source.document_relationship_repositories import (
    DocumentRelationshipRepository,
)
from packages.domain.source.document_relationships import DocumentRelationship
from packages.domain.source.artifacts import SourceArtifact
from packages.domain.source.document_versions import DocumentVersion
from packages.domain.source.extraction import ExtractionRun, ExtractionSegment


@dataclass(frozen=True)
class DocumentProvenance:
    versions: tuple[DocumentVersion, ...]
    artifacts_by_version: dict[str, tuple[SourceArtifact, ...]]
    relationships_by_version: dict[str, tuple[DocumentRelationship, ...]]
    extraction_runs_by_artifact: dict[str, tuple[ExtractionRun, ...]]
    segments_by_extraction: dict[str, tuple[ExtractionSegment, ...]]


class GetDocumentProvenance:
    """Build a read-only document-version/artifact provenance view."""

    def __init__(
        self,
        versions: DocumentVersionRepository,
        artifacts: SourceArtifactRepository,
        relationships: DocumentRelationshipRepository,
        extractions: ExtractionRunRepository,
        segments: ExtractionSegmentRepository,
    ) -> None:
        self.versions = versions
        self.artifacts = artifacts
        self.relationships = relationships
        self.extractions = extractions
        self.segments = segments

    def execute(self, document_id: str) -> DocumentProvenance:
        versions = tuple(self.versions.list_for_document(document_id))
        artifacts = {
            version.id: tuple(self.artifacts.list_for_document_version(version.id))
            for version in versions
        }
        relationships = {
            version.id: tuple(self.relationships.list_for_version(version.id))
            for version in versions
        }
        extraction_runs = {
            artifact.id: tuple(self.extractions.list_for_artifact(artifact.id))
            for version_artifacts in artifacts.values()
            for artifact in version_artifacts
        }
        segments = {
            extraction.id: tuple(self.segments.list_for_extraction(extraction.id))
            for artifact_extractions in extraction_runs.values()
            for extraction in artifact_extractions
        }
        return DocumentProvenance(
            versions=versions,
            artifacts_by_version=artifacts,
            relationships_by_version=relationships,
            extraction_runs_by_artifact=extraction_runs,
            segments_by_extraction=segments,
        )