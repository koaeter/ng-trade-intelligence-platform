"""add requirement scope and evidence

Revision ID: 0002
Revises: 0001_initial_persistence
"""

from alembic import op
import sqlalchemy as sa


revision = "0002"
down_revision = "0001_initial_persistence"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("requirements", sa.Column("product_ids", sa.String(length=2000), nullable=False, server_default=""))
    op.add_column("requirements", sa.Column("hs_codes", sa.String(length=2000), nullable=False, server_default=""))
    op.add_column("requirements", sa.Column("origin_country_codes", sa.String(length=1000), nullable=False, server_default=""))
    op.add_column("requirements", sa.Column("destination_market_codes", sa.String(length=2000), nullable=False, server_default=""))
    op.add_column("requirements", sa.Column("evidence_ids", sa.String(length=4000), nullable=False, server_default=""))
    op.create_table(
        "evidence",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("evidence_type", sa.String(length=64), nullable=False),
        sa.Column("source_id", sa.String(length=64), nullable=False),
        sa.Column("locator", sa.String(length=500), nullable=False),
        sa.Column("excerpt", sa.String(length=4000), nullable=False),
        sa.Column("verified", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("applicability_evaluations", sa.Column("requirement_id", sa.String(length=64), nullable=True))
    op.execute("UPDATE applicability_evaluations SET requirement_id = 'unknown'")
    op.alter_column("applicability_evaluations", "requirement_id", nullable=False)
    op.create_index("ix_applicability_evaluations_requirement_id", "applicability_evaluations", ["requirement_id"])


def downgrade() -> None:
    op.drop_index("ix_applicability_evaluations_requirement_id", table_name="applicability_evaluations")
    op.drop_column("applicability_evaluations", "requirement_id")
    op.drop_table("evidence")
    for column in ["evidence_ids", "destination_market_codes", "origin_country_codes", "hs_codes", "product_ids"]:
        op.drop_column("requirements", column)
