"""add immutable extraction run lineage

Revision ID: 0034
Revises: 0033
"""
from alembic import op
import sqlalchemy as sa


revision = "0034"
down_revision = "0033"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "extraction_runs",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column(
            "artifact_id",
            sa.String(length=64),
            sa.ForeignKey("source_artifacts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "document_version_id",
            sa.String(length=64),
            sa.ForeignKey("document_versions.id"),
            nullable=True,
        ),
        sa.Column("input_checksum_sha256", sa.String(length=64), nullable=False),
        sa.Column("extractor", sa.String(length=128), nullable=False),
        sa.Column("extractor_version", sa.String(length=64), nullable=False),
        sa.Column("extracted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ocr_used", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_index("ix_extraction_runs_artifact_id", "extraction_runs", ["artifact_id"])
    op.create_index("ix_extraction_runs_document_version_id", "extraction_runs", ["document_version_id"])
    op.create_index("ix_extraction_runs_input_checksum", "extraction_runs", ["input_checksum_sha256"])

    op.add_column(
        "extraction_segments",
        sa.Column(
            "extraction_id",
            sa.String(length=64),
            sa.ForeignKey("extraction_runs.id", ondelete="CASCADE"),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_extraction_segments_extraction_id",
        "extraction_segments",
        ["extraction_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_extraction_segments_extraction_id", table_name="extraction_segments")
    op.drop_column("extraction_segments", "extraction_id")
    op.drop_index("ix_extraction_runs_input_checksum", table_name="extraction_runs")
    op.drop_index("ix_extraction_runs_document_version_id", table_name="extraction_runs")
    op.drop_index("ix_extraction_runs_artifact_id", table_name="extraction_runs")
    op.drop_table("extraction_runs")
