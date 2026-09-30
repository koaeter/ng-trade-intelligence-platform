"""add extraction comparison records

Revision ID: 0035
Revises: 0034
"""
from alembic import op
import sqlalchemy as sa

revision = "0035"
down_revision = "0034"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "extraction_comparisons",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("baseline_extraction_id", sa.String(length=64), sa.ForeignKey("extraction_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("candidate_extraction_id", sa.String(length=64), sa.ForeignKey("extraction_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("baseline_input_checksum_sha256", sa.String(length=64), nullable=False),
        sa.Column("candidate_input_checksum_sha256", sa.String(length=64), nullable=False),
        sa.Column("baseline_output_sha256", sa.String(length=64), nullable=False),
        sa.Column("candidate_output_sha256", sa.String(length=64), nullable=False),
        sa.Column("result", sa.String(length=64), nullable=False),
        sa.Column("compared_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_extraction_comparisons_baseline", "extraction_comparisons", ["baseline_extraction_id"])
    op.create_index("ix_extraction_comparisons_candidate", "extraction_comparisons", ["candidate_extraction_id"])
    op.create_index("ix_extraction_comparisons_result", "extraction_comparisons", ["result"])
    op.create_unique_constraint(
        "uq_extraction_comparison_pair",
        "extraction_comparisons",
        ["baseline_extraction_id", "candidate_extraction_id"],
    )

def downgrade() -> None:
    op.drop_constraint("uq_extraction_comparison_pair", "extraction_comparisons", type_="unique")
    op.drop_index("ix_extraction_comparisons_result", table_name="extraction_comparisons")
    op.drop_index("ix_extraction_comparisons_candidate", table_name="extraction_comparisons")
    op.drop_index("ix_extraction_comparisons_baseline", table_name="extraction_comparisons")
    op.drop_table("extraction_comparisons")
