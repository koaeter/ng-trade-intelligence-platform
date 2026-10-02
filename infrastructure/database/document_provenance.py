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
        return int(\n            self._session.scalar(\n                select(func.count()).select_from(model).where(criterion)\n            )\n            or 0\n        )

    def get_summary(self, document_id: str) -> DocumentProvenanceSummary | None:
        if self._session.get(DocumentModel, document_id) is None:
            return None

        versions = select(DocumentVersionModel.id).where(\n            DocumentVersionModel.document_id == document_id\n        )
        artifacts = select(SourceArtifactModel.id).where(\n            SourceArtifactModel.document_version_id.in_(versions)\n        )
        extractions = select(ExtractionRunModel.id).where(\n            ExtractionRunModel.artifact_id.in_(artifacts)\n        )
        comparisons = select(ExtractionComparisonModel.id).where(
            or_(
                ExtractionComparisonModel.baseline_extraction_id.in_(extractions),
                ExtractionComparisonModel.candidate_extraction_id.in_(extractions),
            )
        )
        diffs = select(ExtractionDiffModel.id).where(\n            ExtractionDiffModel.comparison_id.in_(comparisons)\n        )

        return DocumentProvenanceSummary(
            document_id=document_id,
            version_count=self._count(\n                DocumentVersionModel, DocumentVersionModel.document_id == document_id\n            ),
            artifact_count=self._count(\n                SourceArtifactModel, SourceArtifactModel.document_version_id.in_(versions)\n            ),
            relationship_count=self._count(
                DocumentRelationshipModel,
                or_(
                    DocumentRelationshipModel.from_version_id.in_(versions),
                    DocumentRelationshipModel.to_version_id.in_(versions),
                ),
            ),
            extraction_run_count=self._count(\n                ExtractionRunModel, ExtractionRunModel.artifact_id.in_(artifacts)\n            ),
            segment_count=self._count(\n                ExtractionSegmentModel, ExtractionSegmentModel.extraction_id.in_(extractions)\n            ),
            comparison_count=self._count(
                ExtractionComparisonModel,
                or_(
                    ExtractionComparisonModel.baseline_extraction_id.in_(extractions),
                    ExtractionComparisonModel.candidate_extraction_id.in_(extractions),
                ),
            ),
            diff_count=self._count(\n                ExtractionDiffModel, ExtractionDiffModel.comparison_id.in_(comparisons)\n            ),
            diff_entry_count=self._count(\n                ExtractionDiffEntryModel, ExtractionDiffEntryModel.diff_id.in_(diffs)\n            ),
        )
