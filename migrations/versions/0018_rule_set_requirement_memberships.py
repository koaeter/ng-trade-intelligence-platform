"""persist immutable rule-set requirement membership

Revision ID: 0018
Revises: 0017
"""
from alembic import op
import sqlalchemy as sa

revision = "0018"
down_revision = "0017"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "rule_set_requirement_memberships",
        sa.Column("rule_set_id", sa.String(64), sa.ForeignKey("rule_set_versions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("requirement_id", sa.String(64), sa.ForeignKey("requirements.id"), nullable=False),
        sa.Column("requirement_revision", sa.String(64), nullable=False),
        sa.PrimaryKeyConstraint("rule_set_id", "requirement_id"),
    )
    op.create_index(
        "ix_rule_set_requirement_memberships_requirement_id",
        "rule_set_requirement_memberships",
        ["requirement_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_rule_set_requirement_memberships_requirement_id",
        table_name="rule_set_requirement_memberships",
    )
    op.drop_table("rule_set_requirement_memberships")
