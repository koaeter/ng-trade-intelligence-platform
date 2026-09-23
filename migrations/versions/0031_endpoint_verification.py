"""add endpoint verification metadata

Revision ID: 0031
Revises: 0030
"""
from alembic import op
import sqlalchemy as sa

revision = "0031"
down_revision = "0030"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("authority_endpoints", sa.Column("verification_status", sa.String(32), nullable=False, server_default="UNVERIFIED"))
    op.add_column("authority_endpoints", sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("authority_endpoints", sa.Column("verification_note", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("authority_endpoints", "verification_note")
    op.drop_column("authority_endpoints", "last_verified_at")
    op.drop_column("authority_endpoints", "verification_status")
