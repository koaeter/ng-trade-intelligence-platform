"""add governed authority registry

Revision ID: 0026
Revises: 0025
"""
from alembic import op
import sqlalchemy as sa

revision = "0026"
down_revision = "0025"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authorities",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("acronym", sa.String(64), nullable=True),
        sa.Column("jurisdiction_id", sa.String(64), sa.ForeignKey("jurisdictions.id"), nullable=False),
        sa.Column("authority_type", sa.String(64), nullable=False),
        sa.Column("official_url", sa.String(1000), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("acronym", name="uq_authorities_acronym"),
    )
    op.create_index("ix_authorities_jurisdiction_id", "authorities", ["jurisdiction_id"])


def downgrade() -> None:
    op.drop_index("ix_authorities_jurisdiction_id", table_name="authorities")
    op.drop_table("authorities")
