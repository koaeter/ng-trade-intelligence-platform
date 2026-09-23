"""persist source acquisition provenance

Revision ID: 0030
Revises: 0029
"""
from alembic import op
import sqlalchemy as sa

revision = "0030"
down_revision = "0029"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("acquisition_events",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("source_id", sa.String(64), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("endpoint_id", sa.String(64), sa.ForeignKey("authority_endpoints.id"), nullable=True),
        sa.Column("requested_url", sa.String(2000), nullable=False),
        sa.Column("retrieved_url", sa.String(2000), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("http_status", sa.Integer(), nullable=True),
        sa.Column("content_type", sa.String(255), nullable=True),
        sa.Column("content_length", sa.Integer(), nullable=True),
        sa.Column("response_sha256", sa.String(64), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("error_code", sa.String(128), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("artifact_id", sa.String(64), sa.ForeignKey("source_artifacts.id"), nullable=True),
    )
    op.create_index("ix_acquisition_events_source_id", "acquisition_events", ["source_id"])
    op.create_index("ix_acquisition_events_status", "acquisition_events", ["status"])
    op.create_index("ix_acquisition_events_response_sha256", "acquisition_events", ["response_sha256"])
    op.add_column("source_artifacts", sa.Column("acquisition_event_id", sa.String(64), nullable=True))
    op.create_foreign_key("fk_source_artifacts_acquisition_event", "source_artifacts", "acquisition_events", ["acquisition_event_id"], ["id"])
    op.create_index("ix_source_artifacts_acquisition_event_id", "source_artifacts", ["acquisition_event_id"])

def downgrade() -> None:
    op.drop_index("ix_source_artifacts_acquisition_event_id", table_name="source_artifacts")
    op.drop_constraint("fk_source_artifacts_acquisition_event", "source_artifacts", type_="foreignkey")
    op.drop_column("source_artifacts", "acquisition_event_id")
    op.drop_index("ix_acquisition_events_response_sha256", table_name="acquisition_events")
    op.drop_index("ix_acquisition_events_status", table_name="acquisition_events")
    op.drop_index("ix_acquisition_events_source_id", table_name="acquisition_events")
    op.drop_table("acquisition_events")
