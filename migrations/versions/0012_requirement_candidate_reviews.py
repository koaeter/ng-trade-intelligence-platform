"""persist requirement candidate publication reviews

Revision ID: 0012
Revises: 0011
"""
from alembic import op
import sqlalchemy as sa

revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "requirement_candidate_reviews",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("candidate_id", sa.String(64), sa.ForeignKey("requirement_candidates.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reviewer_reference", sa.String(255), nullable=False),
        sa.Column("scope_reviewed", sa.Boolean(), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_requirement_candidate_reviews_candidate_id",
        "requirement_candidate_reviews",
        ["candidate_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_requirement_candidate_reviews_candidate_id",
        table_name="requirement_candidate_reviews",
    )
    op.drop_table("requirement_candidate_reviews")
