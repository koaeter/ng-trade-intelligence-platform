"""support deterministic authority resolution

Revision ID: 0025
Revises: 0024
"""
from alembic import op

revision = "0025"
down_revision = "0024"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "ix_source_authority_resolution_scope",
        "source_authority_assignments",
        ["jurisdiction", "domain", "fact_type", "effective_from", "effective_to", "precedence", "legal_weight"],
    )


def downgrade() -> None:
    op.drop_index("ix_source_authority_resolution_scope", table_name="source_authority_assignments")
