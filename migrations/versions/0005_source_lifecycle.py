"""add source lifecycle state

Revision ID: 0005
Revises: 0004
"""

from alembic import op
import sqlalchemy as sa

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "sources",
        sa.Column("status", sa.String(32), nullable=False, server_default="DISCOVERED"),
    )


def downgrade() -> None:
    op.drop_column("sources", "status")
