"""add governed fact type registry

Revision ID: 0024
Revises: 0023
"""
from alembic import op
import sqlalchemy as sa

revision = "0024"
down_revision = "0023"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "fact_types",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("code", name="uq_fact_types_code"),
    )
    op.create_index("ix_fact_types_code", "fact_types", ["code"])


def downgrade() -> None:
    op.drop_index("ix_fact_types_code", table_name="fact_types")
    op.drop_table("fact_types")
