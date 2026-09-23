"""link sources to authority endpoints

Revision ID: 0029
Revises: 0028
"""
from alembic import op
import sqlalchemy as sa

revision = "0029"
down_revision = "0028"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("sources", sa.Column("endpoint_id", sa.String(64), nullable=True))
    op.create_foreign_key("fk_sources_endpoint_id", "sources", "authority_endpoints", ["endpoint_id"], ["id"])
    op.create_index("ix_sources_endpoint_id", "sources", ["endpoint_id"])


def downgrade() -> None:
    op.drop_index("ix_sources_endpoint_id", table_name="sources")
    op.drop_constraint("fk_sources_endpoint_id", "sources", type_="foreignkey")
    op.drop_column("sources", "endpoint_id")
