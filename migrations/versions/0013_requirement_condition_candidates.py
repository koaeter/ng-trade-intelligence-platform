"""persist structured requirement condition candidates

Revision ID: 0013
Revises: 0012
"""
from alembic import op
import sqlalchemy as sa

revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "requirement_condition_candidates",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("candidate_id", sa.String(64), sa.ForeignKey("requirement_candidates.id", ondelete="CASCADE"), nullable=False),
        sa.Column("field", sa.String(64), nullable=False),
        sa.Column("operator", sa.String(64), nullable=False),
        sa.Column("value", sa.Text(), nullable=True),
    )
    op.create_index(
        "ix_requirement_condition_candidates_candidate_id",
        "requirement_condition_candidates",
        ["candidate_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_requirement_condition_candidates_candidate_id",
        table_name="requirement_condition_candidates",
    )
    op.drop_table("requirement_condition_candidates")
