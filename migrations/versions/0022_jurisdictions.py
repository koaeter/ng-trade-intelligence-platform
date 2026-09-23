"""add hierarchical jurisdiction registry

Revision ID: 0022
Revises: 0021
"""
from alembic import op
import sqlalchemy as sa

revision = "0022"
down_revision = "0021"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "jurisdictions",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("jurisdiction_type", sa.String(32), nullable=False),
        sa.Column("code", sa.String(64), nullable=True),
        sa.Column("parent_id", sa.String(64), sa.ForeignKey("jurisdictions.id"), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("code", name="uq_jurisdictions_code"),
    )
    op.create_index("ix_jurisdictions_jurisdiction_type", "jurisdictions", ["jurisdiction_type"])
    op.create_index("ix_jurisdictions_code", "jurisdictions", ["code"])


def downgrade() -> None:
    op.drop_index("ix_jurisdictions_code", table_name="jurisdictions")
    op.drop_index("ix_jurisdictions_jurisdiction_type", table_name="jurisdictions")
    op.drop_table("jurisdictions")
