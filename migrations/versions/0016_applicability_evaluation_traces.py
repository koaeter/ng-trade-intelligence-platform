"""persist deterministic applicability traces

Revision ID: 0016
Revises: 0015
"""
from alembic import op
import sqlalchemy as sa

revision = "0016"
down_revision = "0015"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "applicability_evaluation_traces",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("scenario_id", sa.String(64), sa.ForeignKey("export_scenarios.id"), nullable=False),
        sa.Column("requirement_id", sa.String(64), sa.ForeignKey("requirements.id"), nullable=False),
        sa.Column("rule_set_version", sa.String(64), nullable=False),
        sa.Column("scenario_date", sa.Date(), nullable=False),
        sa.Column("temporal_result", sa.String(16), nullable=False),
        sa.Column("scope_result", sa.String(16), nullable=False),
        sa.Column("condition_result", sa.String(16), nullable=False),
        sa.Column("evidence_result", sa.String(32), nullable=False),
        sa.Column("final_result", sa.String(32), nullable=False),
    )
    op.create_index(
        "ix_applicability_evaluation_traces_scenario_id",
        "applicability_evaluation_traces",
        ["scenario_id"],
    )
    op.create_index(
        "ix_applicability_evaluation_traces_requirement_id",
        "applicability_evaluation_traces",
        ["requirement_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_applicability_evaluation_traces_requirement_id",
        table_name="applicability_evaluation_traces",
    )
    op.drop_index(
        "ix_applicability_evaluation_traces_scenario_id",
        table_name="applicability_evaluation_traces",
    )
    op.drop_table("applicability_evaluation_traces")
