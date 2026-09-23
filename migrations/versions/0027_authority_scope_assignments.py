"""add authority regulatory scope assignments

Revision ID: 0027
Revises: 0026
"""
from alembic import op
import sqlalchemy as sa

revision = "0027"
down_revision = "0026"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authority_scope_assignments",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("authority_id", sa.String(64), sa.ForeignKey("authorities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("jurisdiction_id", sa.String(64), sa.ForeignKey("jurisdictions.id"), nullable=False),
        sa.Column("regulatory_domain_code", sa.String(64), nullable=False),
        sa.Column("fact_type_code", sa.String(64), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.UniqueConstraint(
            "authority_id", "jurisdiction_id", "regulatory_domain_code", "fact_type_code",
            name="uq_authority_scope_assignment",
        ),
    )
    op.create_index(
        "ix_authority_scope_domain_fact",
        "authority_scope_assignments",
        ["jurisdiction_id", "regulatory_domain_code", "fact_type_code"],
    )


def downgrade() -> None:
    op.drop_index("ix_authority_scope_domain_fact", table_name="authority_scope_assignments")
    op.drop_table("authority_scope_assignments")
