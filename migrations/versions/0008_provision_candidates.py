"""persist reviewable provision candidates

Revision ID: 0008
Revises: 0007
"""
from alembic import op
import sqlalchemy as sa

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "provision_candidates",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("document_id", sa.String(64), sa.ForeignKey("documents.id"), nullable=False),
        sa.Column(
            "artifact_id",
            sa.String(64),
            sa.ForeignKey("source_artifacts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "extraction_segment_id",
            sa.String(64),
            sa.ForeignKey("extraction_segments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("locator", sa.String(1000), nullable=False),
        sa.Column("candidate_type", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.UniqueConstraint(
            "document_id",
            "extraction_segment_id",
            name="uq_provision_candidates_document_segment",
        ),
    )
    op.create_index(
        "ix_provision_candidates_document_id",
        "provision_candidates",
        ["document_id"],
    )
    op.create_index(
        "ix_provision_candidates_artifact_id",
        "provision_candidates",
        ["artifact_id"],
    )
    op.create_index(
        "ix_provision_candidates_status",
        "provision_candidates",
        ["status"],
    )


def downgrade() -> None:
    op.drop_index("ix_provision_candidates_status", table_name="provision_candidates")
    op.drop_index("ix_provision_candidates_artifact_id", table_name="provision_candidates")
    op.drop_index("ix_provision_candidates_document_id", table_name="provision_candidates")
    op.drop_table("provision_candidates")
