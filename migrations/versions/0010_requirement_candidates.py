"""persist reviewable requirement candidates

Revision ID: 0010
Revises: 0009
"""
from alembic import op
import sqlalchemy as sa

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "requirement_candidates",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column(
            "provision_id",
            sa.String(64),
            sa.ForeignKey("provisions.id"),
            nullable=False,
        ),
        sa.Column(
            "document_id",
            sa.String(64),
            sa.ForeignKey("documents.id"),
            nullable=False,
        ),
        sa.Column("proposed_name", sa.String(255), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.UniqueConstraint(
            "provision_id",
            name="uq_requirement_candidates_provision",
        ),
    )
    op.create_index(
        "ix_requirement_candidates_provision_id",
        "requirement_candidates",
        ["provision_id"],
    )
    op.create_index(
        "ix_requirement_candidates_document_id",
        "requirement_candidates",
        ["document_id"],
    )
    op.create_index(
        "ix_requirement_candidates_status",
        "requirement_candidates",
        ["status"],
    )


def downgrade() -> None:
    op.drop_index("ix_requirement_candidates_status", table_name="requirement_candidates")
    op.drop_index("ix_requirement_candidates_document_id", table_name="requirement_candidates")
    op.drop_index("ix_requirement_candidates_provision_id", table_name="requirement_candidates")
    op.drop_table("requirement_candidates")
