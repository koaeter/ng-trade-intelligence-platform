"""persist normalized requirement rule trees

Revision ID: 0015
Revises: 0014
"""
from alembic import op
import sqlalchemy as sa

revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "requirement_rule_nodes",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("requirement_id", sa.String(64), sa.ForeignKey("requirements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("parent_id", sa.String(64), nullable=True),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("node_type", sa.String(32), nullable=False),
        sa.Column("group_operator", sa.String(16), nullable=True),
        sa.Column("field", sa.String(64), nullable=True),
        sa.Column("operator", sa.String(64), nullable=True),
        sa.Column("value", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["requirement_rule_nodes.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("requirement_id", "parent_id", "sequence", name="uq_requirement_rule_nodes_order"),
    )
    op.create_index(
        "ix_requirement_rule_nodes_requirement_id",
        "requirement_rule_nodes",
        ["requirement_id"],
    )
    op.create_index(
        "ix_requirement_rule_nodes_parent_id",
        "requirement_rule_nodes",
        ["parent_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_requirement_rule_nodes_parent_id", table_name="requirement_rule_nodes")
    op.drop_index("ix_requirement_rule_nodes_requirement_id", table_name="requirement_rule_nodes")
    op.drop_table("requirement_rule_nodes")
