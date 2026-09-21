"""add source document provision provenance

Revision ID: 0004
Revises: 0003
"""

from alembic import op
import sqlalchemy as sa

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("organization", sa.String(255), nullable=False),
        sa.Column("source_type", sa.String(64), nullable=False),
        sa.Column("jurisdiction", sa.String(128), nullable=True),
        sa.Column("official_url", sa.String(1000), nullable=True),
    )
    op.create_table(
        "documents",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("source_id", sa.String(64), sa.ForeignKey("sources.id"), nullable=False, index=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("document_type", sa.String(64), nullable=False),
        sa.Column("publication_date", sa.Date(), nullable=True),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("version_label", sa.String(128), nullable=True),
    )
    op.create_table(
        "provisions",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("document_id", sa.String(64), sa.ForeignKey("documents.id"), nullable=False, index=True),
        sa.Column("locator", sa.String(500), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("provision_type", sa.String(64), nullable=False),
    )
    op.add_column("evidence", sa.Column("document_id", sa.String(64), nullable=True))
    op.add_column("evidence", sa.Column("provision_id", sa.String(64), nullable=True))
    op.create_foreign_key("fk_evidence_source", "evidence", "sources", ["source_id"], ["id"])
    op.create_foreign_key("fk_evidence_document", "evidence", "documents", ["document_id"], ["id"])
    op.create_foreign_key("fk_evidence_provision", "evidence", "provisions", ["provision_id"], ["id"])
    op.create_index("ix_evidence_document_id", "evidence", ["document_id"])
    op.create_index("ix_evidence_provision_id", "evidence", ["provision_id"])
    op.create_foreign_key("fk_requirement_hs_code", "requirement_hs_codes", "hs_codes", ["hs_version_id", "hs_code"], ["version_id", "code"])


def downgrade() -> None:
    op.drop_constraint("fk_requirement_hs_code", "requirement_hs_codes", type_="foreignkey")
    op.drop_index("ix_evidence_provision_id", table_name="evidence")
    op.drop_index("ix_evidence_document_id", table_name="evidence")
    op.drop_constraint("fk_evidence_provision", "evidence", type_="foreignkey")
    op.drop_constraint("fk_evidence_document", "evidence", type_="foreignkey")
    op.drop_constraint("fk_evidence_source", "evidence", type_="foreignkey")
    op.drop_column("evidence", "provision_id")
    op.drop_column("evidence", "document_id")
    op.drop_table("provisions")
    op.drop_table("documents")
    op.drop_table("sources")
