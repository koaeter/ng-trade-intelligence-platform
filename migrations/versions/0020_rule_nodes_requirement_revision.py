"""bind requirement rule nodes to immutable revisions

Revision ID: 0020
Revises: 0019
"""
from alembic import op
import sqlalchemy as sa

revision = "0020"
down_revision = "0019"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "requirement_rule_nodes",
        sa.Column("requirement_revision_id", sa.String(64), nullable=True),
    )
    op.create_index(
        "ix_requirement_rule_nodes_requirement_revision_id",
        "requirement_rule_nodes",
        ["requirement_revision_id"],
    )
    op.create_foreign_key(
        "fk_requirement_rule_nodes_revision",
        "requirement_rule_nodes",
        "requirement_revisions",
        ["requirement_revision_id"],
        ["id"],
    )
    # Existing nodes may remain unbound. The application loader rejects them
    # for historical evaluation until a revision is explicitly assigned.


def downgrade() -> None:
    op.drop_constraint("fk_requirement_rule_nodes_revision", "requirement_rule_nodes", type_="foreignkey")
    op.drop_index("ix_requirement_rule_nodes_requirement_revision_id", table_name="requirement_rule_nodes")
    op.drop_column("requirement_rule_nodes", "requirement_revision_id")
