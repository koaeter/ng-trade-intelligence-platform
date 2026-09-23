"""persist immutable requirement revisions

Revision ID: 0019
Revises: 0018
"""
from alembic import op
import sqlalchemy as sa

revision = "0019"
down_revision = "0018"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "requirement_revisions",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("requirement_id", sa.String(64), sa.ForeignKey("requirements.id"), nullable=False),
        sa.Column("revision", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("product_ids", sa.JSON(), nullable=False),
        sa.Column("hs_codes", sa.JSON(), nullable=False),
        sa.Column("origin_country_codes", sa.JSON(), nullable=False),
        sa.Column("destination_market_codes", sa.JSON(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("scope_is_general", sa.Boolean(), nullable=False),
        sa.UniqueConstraint("requirement_id", "revision", name="uq_requirement_revisions_version"),
    )
    op.create_index(
        "ix_requirement_revisions_requirement_id",
        "requirement_revisions",
        ["requirement_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_requirement_revisions_requirement_id",
        table_name="requirement_revisions",
    )
    op.drop_table("requirement_revisions")
