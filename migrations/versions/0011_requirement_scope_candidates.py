"""persist structured requirement scope candidates

Revision ID: 0011
Revises: 0010
"""
from alembic import op
import sqlalchemy as sa

revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "requirement_scope_candidates",
        sa.Column("candidate_id", sa.String(64), sa.ForeignKey("requirement_candidates.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("product_ids", sa.JSON(), nullable=False),
        sa.Column("hs_codes", sa.JSON(), nullable=False),
        sa.Column("origin_country_codes", sa.JSON(), nullable=False),
        sa.Column("destination_market_codes", sa.JSON(), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("conditions", sa.JSON(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("requirement_scope_candidates")
