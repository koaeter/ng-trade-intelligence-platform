"""add source authority matrix and instrument metadata

Revision ID: 0021
Revises: 0020
"""
from alembic import op
import sqlalchemy as sa

revision = "0021"
down_revision = "0020"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "source_authority_assignments",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("source_id", sa.String(64), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("authority_type", sa.String(64), nullable=False),
        sa.Column("jurisdiction", sa.String(128), nullable=False),
        sa.Column("domain", sa.String(128), nullable=False),
        sa.Column("fact_type", sa.String(128), nullable=False),
        sa.Column("precedence", sa.Integer(), nullable=False),
        sa.Column("legal_weight", sa.Integer(), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("verification_status", sa.String(32), nullable=False),
        sa.Column("supersedes_assignment_id", sa.String(64), sa.ForeignKey("source_authority_assignments.id"), nullable=True),
        sa.UniqueConstraint("source_id", "jurisdiction", "domain", "fact_type", "effective_from", name="uq_source_authority_scope"),
    )
    for column in ("source_id", "jurisdiction", "domain", "fact_type"):
        op.create_index(f"ix_source_authority_assignments_{column}", "source_authority_assignments", [column])

    op.create_table(
        "instruments",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("document_id", sa.String(64), sa.ForeignKey("documents.id"), nullable=False),
        sa.Column("instrument_type", sa.String(64), nullable=False),
        sa.Column("legal_effect", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="ACTIVE"),
        sa.Column("parties", sa.JSON(), nullable=False),
        sa.Column("supersedes_instrument_id", sa.String(64), sa.ForeignKey("instruments.id"), nullable=True),
        sa.UniqueConstraint("document_id", name="uq_instruments_document_id"),
    )
    for column in ("document_id", "instrument_type", "legal_effect"):
        op.create_index(f"ix_instruments_{column}", "instruments", [column])


def downgrade() -> None:
    for column in ("legal_effect", "instrument_type", "document_id"):
        op.drop_index(f"ix_instruments_{column}", table_name="instruments")
    op.drop_table("instruments")
    for column in ("fact_type", "domain", "jurisdiction", "source_id"):
        op.drop_index(f"ix_source_authority_assignments_{column}", table_name="source_authority_assignments")
    op.drop_table("source_authority_assignments")
