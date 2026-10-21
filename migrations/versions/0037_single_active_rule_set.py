"""enforce at most one active rule set

Revision ID: 0037
Revises: 0036
"""
import sqlalchemy as sa
from alembic import op

revision = "0037"
down_revision = "0036"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # A partial unique index prevents concurrent requests from activating
    # different versions at the same time. Existing duplicate ACTIVE rows, if
    # present, must be reconciled before this migration can be applied.
    op.create_index(
        "uq_rule_set_versions_single_active",
        "rule_set_versions",
        ["status"],
        unique=True,
        postgresql_where=sa.text("status = 'ACTIVE'"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_rule_set_versions_single_active",
        table_name="rule_set_versions",
    )
