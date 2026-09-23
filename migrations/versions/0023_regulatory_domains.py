"""add governed regulatory domain registry

Revision ID: 0023
Revises: 0022
"""
from alembic import op
import sqlalchemy as sa

revision = "0023"
down_revision = "0022"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "regulatory_domains",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("parent_id", sa.String(64), sa.ForeignKey("regulatory_domains.id"), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("code", name="uq_regulatory_domains_code"),
    )
    op.create_index("ix_regulatory_domains_code", "regulatory_domains", ["code"])


def downgrade() -> None:
    op.drop_index("ix_regulatory_domains_code", table_name="regulatory_domains")
    op.drop_table("regulatory_domains")
