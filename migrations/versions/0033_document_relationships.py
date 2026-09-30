"""add explicit document version relationships

Revision ID: 0033
Revises: 0032
"""
from alembic import op
import sqlalchemy as sa


revision = "0033"
down_revision = "0032"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "document_relationships",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("relationship_type", sa.String(length=32), nullable=False),
        sa.Column(
            "from_version_id",
            sa.String(length=64),
            sa.ForeignKey("document_versions.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "to_version_id",
            sa.String(length=64),
            sa.ForeignKey("document_versions.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("evidence_reference", sa.String(length=1000), nullable=True),
        sa.Column("note", sa.String(length=2000), nullable=True),
    )
    op.create_index(
        "ix_document_relationships_from_to",
        "document_relationships",
        ["from_version_id", "to_version_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_document_relationships_from_to", table_name="document_relationships")
    op.drop_table("document_relationships")
