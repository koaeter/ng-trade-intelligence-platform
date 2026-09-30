"""add immutable document version lineage

Revision ID: 0032
Revises: 0031
"""
from alembic import op
import sqlalchemy as sa


revision = "0032"
down_revision = "0031"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "document_versions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column(
            "document_id",
            sa.String(length=64),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("version_label", sa.String(length=128), nullable=True),
        sa.Column("publication_date", sa.Date(), nullable=True),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("revision_reference", sa.String(length=255), nullable=True),
    )
    op.create_index(
        "ix_document_versions_document_effective_from",
        "document_versions",
        ["document_id", "effective_from"],
    )
    op.add_column(
        "source_artifacts",
        sa.Column(
            "document_version_id",
            sa.String(length=64),
            sa.ForeignKey("document_versions.id"),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_source_artifacts_document_version_id",
        "source_artifacts",
        ["document_version_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_source_artifacts_document_version_id", table_name="source_artifacts")
    op.drop_column("source_artifacts", "document_version_id")
    op.drop_index(
        "ix_document_versions_document_effective_from",
        table_name="document_versions",
    )
    op.drop_table("document_versions")
