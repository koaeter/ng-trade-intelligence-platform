from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from infrastructure.database.models import (
    DocumentModel,
    DocumentVersionModel,
    DocumentRelationshipModel,
    SourceArtifactModel,
    ExtractionRunModel,
    ExtractionSegmentModel,
    ExtractionComparisonModel,
    ExtractionDiffModel,
    ExtractionDiffEntryModel,
)
from packages.application.source.document_provenance_summary import DocumentProvenanceSummary


class SqlAlchemyDocumentProvenanceSummaryRepository:
    """Count-only provenance projection using database aggregates."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def _count(self, model, criterion) -> int:
        return int(
            self._session.scalar(
                select(func.count()).select_from(model).where(criterion)
            )
            or 0
        )

    def get_summary(self, document_id: str) -> DocumentProvenanceSummary | None:
        if self._session.get(DocumentModel, document_id) is None:
            return None

        versions = select(DocumentVersionModel.id).where(
            DocumentVersionModel.document_id == document_id
        )
        artifacts = select(SourceArtifactModel.id).where(
            SourceArtifactModel.document_version_id.in_(versions)
        )
        extractions = select(ExtractionRunModel.id).where(
            ExtractionRunModel.artifact_id.in_(artifacts)
        )
        comparisons = select(ExtractionComparisonModel.id).where(
            or_(
                ExtractionComparisonModel.baseline_extraction_id.in_(extractions),
                ExtractionComparisonModel.candidate_extraction_id.in_(extractions),
            )
        )
        diffs = select(ExtractionDiffModel.id).where(
            ExtractionDiffModel.comparison_id.in_(comparisons)
        )

        return DocumentProvenanceSummary(
            document_id=document_id,
            version_count=self._count(
                DocumentVersionModel, DocumentVersionModel.document_id == document_id
            ),
            artifact_count=self._count(
                SourceArtifactModel, SourceArtifactModel.document_version_id.in_(versions)
            ),
            relationship_count=self._count(
                DocumentRelationshipModel,
                or_(
                    DocumentRelationshipModel.from_version_id.in_(versions),
                    DocumentRelationshipModel.to_version_id.in_(versions),
                ),
            ),
            extraction_run_count=self._count(
                ExtractionRunModel, ExtractionRunModel.artifact_id.in_(artifacts)
            ),
            segment_count=self._count(
                ExtractionSegmentModel, ExtractionSegmentModel.extraction_id.in_(extractions)
            ),
            comparison_count=self._count(
                ExtractionComparisonModel,
                or_(
                    ExtractionComparisonModel.baseline_extraction_id.in_(extractions),
                    ExtractionComparisonModel.candidate_extraction_id.in_(extractions),
                ),
            ),
            diff_count=self._count(
                ExtractionDiffModel, ExtractionDiffModel.comparison_id.in_(comparisons)
            ),
            diff_entry_count=self._count(
                ExtractionDiffEntryModel, ExtractionDiffEntryModel.diff_id.in_(diffs)
            ),
        )
