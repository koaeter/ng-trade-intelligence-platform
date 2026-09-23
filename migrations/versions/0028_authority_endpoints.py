"""add authority source endpoints

Revision ID: 0028
Revises: 0027
"""
from alembic import op
import sqlalchemy as sa

revision = "0028"
down_revision = "0027"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authority_endpoints",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("authority_id", sa.String(64), sa.ForeignKey("authorities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("url", sa.String(2000), nullable=False),
        sa.Column("endpoint_type", sa.String(64), nullable=False),
        sa.Column("access_method", sa.String(64), nullable=False),
        sa.Column("content_format", sa.String(64), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.UniqueConstraint("authority_id", "url", name="uq_authority_endpoint_url"),
    )
    op.create_index(
        "ix_authority_endpoint_type",
        "authority_endpoints",
        ["authority_id", "endpoint_type"],
    )


def downgrade() -> None:
    op.drop_index("ix_authority_endpoint_type", table_name="authority_endpoints")
    op.drop_table("authority_endpoints")
