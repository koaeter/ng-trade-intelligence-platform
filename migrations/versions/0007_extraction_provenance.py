"""persist extraction segments and source locations

Revision ID: 0007
Revises: 0006
"""
from alembic import op
import sqlalchemy as sa
revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("extraction_segments",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("artifact_id", sa.String(64), sa.ForeignKey("source_artifacts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column("section", sa.String(1000), nullable=True),
        sa.Column("source_start", sa.Integer(), nullable=True),
        sa.Column("source_end", sa.Integer(), nullable=True),
        sa.Column("locator", sa.String(1000), nullable=True),
        sa.UniqueConstraint("artifact_id", "sequence", name="uq_extraction_segments_artifact_sequence"),
    )
    op.create_index("ix_extraction_segments_artifact_id", "extraction_segments", ["artifact_id"])
    op.create_index("ix_extraction_segments_page_number", "extraction_segments", ["page_number"])

def downgrade() -> None:
    op.drop_index("ix_extraction_segments_page_number", table_name="extraction_segments")
    op.drop_index("ix_extraction_segments_artifact_id", table_name="extraction_segments")
    op.drop_table("extraction_segments")
