"""add segment-level extraction diffs

Revision ID: 0036
Revises: 0035
"""
from alembic import op
import sqlalchemy as sa

revision = "0036"
down_revision = "0035"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "extraction_diffs",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("comparison_id", sa.String(length=64), sa.ForeignKey("extraction_comparisons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("baseline_extraction_id", sa.String(length=64), sa.ForeignKey("extraction_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("candidate_extraction_id", sa.String(length=64), sa.ForeignKey("extraction_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entry_count", sa.Integer(), nullable=False),
        sa.Column("unchanged_count", sa.Integer(), nullable=False),
        sa.Column("added_count", sa.Integer(), nullable=False),
        sa.Column("removed_count", sa.Integer(), nullable=False),
        sa.Column("modified_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_extraction_diffs_comparison", "extraction_diffs", ["comparison_id"])
    op.create_index("ix_extraction_diffs_baseline", "extraction_diffs", ["baseline_extraction_id"])
    op.create_index("ix_extraction_diffs_candidate", "extraction_diffs", ["candidate_extraction_id"])

    op.create_table(
        "extraction_diff_entries",
        sa.Column("id", sa.String(length=128), primary_key=True),
        sa.Column("diff_id", sa.String(length=64), sa.ForeignKey("extraction_diffs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entry_type", sa.String(length=32), nullable=False),
        sa.Column("ordinal", sa.Integer(), nullable=False),
        sa.Column("baseline_segment_id", sa.String(length=64), sa.ForeignKey("extraction_segments.id", ondelete="SET NULL")),
        sa.Column("candidate_segment_id", sa.String(length=64), sa.ForeignKey("extraction_segments.id", ondelete="SET NULL")),
        sa.Column("baseline_sequence", sa.Integer()),
        sa.Column("candidate_sequence", sa.Integer()),
        sa.Column("baseline_text_sha256", sa.String(length=64)),
        sa.Column("candidate_text_sha256", sa.String(length=64)),
        sa.Column("baseline_page_number", sa.Integer()),
        sa.Column("candidate_page_number", sa.Integer()),
        sa.Column("baseline_section", sa.String(length=1000)),
        sa.Column("candidate_section", sa.String(length=1000)),
        sa.Column("baseline_source_start", sa.Integer()),
        sa.Column("baseline_source_end", sa.Integer()),
        sa.Column("candidate_source_start", sa.Integer()),
        sa.Column("candidate_source_end", sa.Integer()),
        sa.Column("baseline_locator", sa.String(length=1000)),
        sa.Column("candidate_locator", sa.String(length=1000)),
    )
    op.create_index("ix_extraction_diff_entries_diff", "extraction_diff_entries", ["diff_id"])
    op.create_index("ix_extraction_diff_entries_type", "extraction_diff_entries", ["entry_type"])
    op.create_index("ix_extraction_diff_entries_baseline_segment", "extraction_diff_entries", ["baseline_segment_id"])
    op.create_index("ix_extraction_diff_entries_candidate_segment", "extraction_diff_entries", ["candidate_segment_id"])
    op.create_unique_constraint(
        "uq_extraction_diff_entry_ordinal",
        "extraction_diff_entries",
        ["diff_id", "ordinal"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_extraction_diff_entry_ordinal", "extraction_diff_entries", type_="unique")
    op.drop_index("ix_extraction_diff_entries_candidate_segment", table_name="extraction_diff_entries")
    op.drop_index("ix_extraction_diff_entries_baseline_segment", table_name="extraction_diff_entries")
    op.drop_index("ix_extraction_diff_entries_type", table_name="extraction_diff_entries")
    op.drop_index("ix_extraction_diff_entries_diff", table_name="extraction_diff_entries")
    op.drop_table("extraction_diff_entries")
    op.drop_index("ix_extraction_diffs_candidate", table_name="extraction_diffs")
    op.drop_index("ix_extraction_diffs_baseline", table_name="extraction_diffs")
    op.drop_index("ix_extraction_diffs_comparison", table_name="extraction_diffs")
    op.drop_table("extraction_diffs")
