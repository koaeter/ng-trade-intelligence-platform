"""persist deterministic rule-set versions

Revision ID: 0017
Revises: 0016
"""
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa

revision = "0017"
down_revision = "0016"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "rule_set_versions",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("version", sa.String(64), nullable=False, unique=True),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.bulk_insert(
        sa.table(
            "rule_set_versions",
            sa.column("id", sa.String),
            sa.column("version", sa.String),
            sa.column("status", sa.String),
            sa.column("created_at", sa.DateTime(timezone=True)),
        ),
        [{
            "id": "rule-set-initial",
            "version": "initial",
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc),
        }],
    )


def downgrade() -> None:
    op.drop_table("rule_set_versions")
