from dataclasses import dataclass

from packages.application.source.artifact_repositories import SourceArtifactRepository
from packages.application.source.extraction_repositories import (
    ExtractionRunRepository,
    ExtractionSegmentRepository,
    ExtractionComparisonRepository,
    ExtractionDiffRepository,
    ExtractionDiffEntryRepository,
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
from packages.domain.source.extraction import ExtractionComparison, ExtractionRun, ExtractionSegment
from packages.domain.source.extraction_diff import ExtractionDiff, ExtractionDiffEntry


@dataclass(frozen=True)
class DocumentProvenance:
    versions: tuple[DocumentVersion, ...]
    artifacts_by_version: dict[str, tuple[SourceArtifact, ...]]
    relationships_by_version: dict[str, tuple[DocumentRelationship, ...]]
    extraction_runs_by_artifact: dict[str, tuple[ExtractionRun, ...]]
    segments_by_extraction: dict[str, tuple[ExtractionSegment, ...]]
    comparisons_by_extraction: dict[str, tuple[ExtractionComparison, ...]]
    diffs_by_comparison: dict[str, tuple[ExtractionDiff, ...]]
    diff_entries_by_diff: dict[str, tuple[ExtractionDiffEntry, ...]]
    truncated_collections: tuple[str, ...]


class GetDocumentProvenance:
    """Build a read-only document-version/artifact provenance view."""

    def __init__(
        self,
        versions: DocumentVersionRepository,
        artifacts: SourceArtifactRepository,
        relationships: DocumentRelationshipRepository,
        extractions: ExtractionRunRepository,
        segments: ExtractionSegmentRepository,
        comparisons: ExtractionComparisonRepository,
        diffs: ExtractionDiffRepository,
        diff_entries: ExtractionDiffEntryRepository,
    ) -> None:
        self.versions = versions
        self.artifacts = artifacts
        self.relationships = relationships
        self.extractions = extractions
        self.segments = segments
        self.comparisons = comparisons
        self.diffs = diffs
        self.diff_entries = diff_entries

    def execute(self, document_id: str, limit: int = 100) -> DocumentProvenance:
        if limit < 1:
            raise ValueError("limit must be at least 1")

        truncated: list[str] = []

        def bounded(items, name: str) -> tuple:
            values = tuple(items)
            if len(values) > limit:
                truncated.append(name)
            return values[:limit]

        versions = bounded(
            self.versions.list_for_document(document_id, limit=limit + 1),
            "versions",
        )
        artifacts = {}
        relationships = {}
        for version in versions:
            artifacts[version.id] = bounded(
                self.artifacts.list_for_document_version(version.id, limit=limit + 1),
                f"artifacts_by_version:{version.id}",
            )
            relationships[version.id] = bounded(
                self.relationships.list_for_version(version.id, limit=limit + 1),
                f"relationships_by_version:{version.id}",
            )

        extraction_runs = {}
        for version_artifacts in artifacts.values():
            for artifact in version_artifacts:
                extraction_runs[artifact.id] = bounded(
                    self.extractions.list_for_artifact(artifact.id, limit=limit + 1),
                    f"extraction_runs_by_artifact:{artifact.id}",
                )

        segments = {}
        comparisons = {}
        for artifact_extractions in extraction_runs.values():
            for extraction in artifact_extractions:
                segments[extraction.id] = bounded(
                    self.segments.list_for_extraction(extraction.id, limit=limit + 1),
                    f"segments_by_extraction:{extraction.id}",
                )
                comparisons[extraction.id] = bounded(
                    self.comparisons.list_for_extraction(extraction.id, limit=limit + 1),
                    f"comparisons_by_extraction:{extraction.id}",
                )

        diffs = {}
        for extraction_comparisons in comparisons.values():
            for comparison in extraction_comparisons:
                diffs[comparison.id] = bounded(
                    self.diffs.list_for_comparison(comparison.id, limit=limit + 1),
                    f"diffs_by_comparison:{comparison.id}",
                )

        diff_entries = {}
        for comparison_diffs in diffs.values():
            for diff in comparison_diffs:
                diff_entries[diff.id] = bounded(
                    self.diff_entries.list_for_diff(diff.id, limit=limit + 1),
                    f"diff_entries_by_diff:{diff.id}",
                )

        return DocumentProvenance(
            versions=versions,
            artifacts_by_version=artifacts,
            relationships_by_version=relationships,
            extraction_runs_by_artifact=extraction_runs,
            segments_by_extraction=segments,
            comparisons_by_extraction=comparisons,
            diffs_by_comparison=diffs,
            diff_entries_by_diff=diff_entries,
            truncated_collections=tuple(truncated),
        )
