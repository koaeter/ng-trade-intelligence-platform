"""persist governed candidate review decisions

Revision ID: 0009
Revises: 0008
"""
from alembic import op
import sqlalchemy as sa

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "provision_candidate_reviews",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "candidate_id",
            sa.String(64),
            sa.ForeignKey("provision_candidates.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("reviewer_reference", sa.String(255), nullable=False),
        sa.Column("decision", sa.String(32), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_provision_candidate_reviews_candidate_id",
        "provision_candidate_reviews",
        ["candidate_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_provision_candidate_reviews_candidate_id",
        table_name="provision_candidate_reviews",
    )
    op.drop_table("provision_candidate_reviews")
