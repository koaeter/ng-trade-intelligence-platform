"""persist source artifacts and extracted text

Revision ID: 0006
Revises: 0005
"""

from alembic import op
import sqlalchemy as sa

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "source_artifacts",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("source_id", sa.String(64), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("document_id", sa.String(64), sa.ForeignKey("documents.id"), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("storage_key", sa.String(1000), nullable=False),
        sa.Column("checksum_sha256", sa.String(64), nullable=False),
        sa.Column("acquired_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("mime_type", sa.String(255), nullable=True),
        sa.Column("original_filename", sa.String(500), nullable=True),
        sa.Column("processing_state", sa.String(32), nullable=False, server_default="ACQUIRED"),
    )
    op.create_index("ix_source_artifacts_source_id", "source_artifacts", ["source_id"])
    op.create_index("ix_source_artifacts_document_id", "source_artifacts", ["document_id"])
    op.create_index("ix_source_artifacts_checksum_sha256", "source_artifacts", ["checksum_sha256"])
    op.create_table(
        "extracted_texts",
        sa.Column("artifact_id", sa.String(64), sa.ForeignKey("source_artifacts.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("extractor", sa.String(128), nullable=False),
        sa.Column("extractor_version", sa.String(64), nullable=False),
        sa.Column("extracted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ocr_used", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_table("extracted_texts")
    op.drop_index("ix_source_artifacts_checksum_sha256", table_name="source_artifacts")
    op.drop_index("ix_source_artifacts_document_id", table_name="source_artifacts")
    op.drop_index("ix_source_artifacts_source_id", table_name="source_artifacts")
    op.drop_table("source_artifacts")
