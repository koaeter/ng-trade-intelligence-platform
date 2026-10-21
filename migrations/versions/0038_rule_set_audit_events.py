"""add append-only rule-set audit events

Revision ID: 0038
Revises: 0037
"""
import sqlalchemy as sa
from alembic import op

revision = "0038"
down_revision = "0037"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "rule_set_audit_events",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("actor_subject", sa.String(length=255), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column(
            "target_rule_set_id",
            sa.String(length=64),
            sa.ForeignKey("rule_set_versions.id"),
            nullable=False,
        ),
        sa.Column("outcome", sa.String(length=16), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("detail", sa.Text(), nullable=True),
    )
    op.create_index(
        "ix_rule_set_audit_events_actor_subject",
        "rule_set_audit_events",
        ["actor_subject"],
    )
    op.create_index(
        "ix_rule_set_audit_events_action",
        "rule_set_audit_events",
        ["action"],
    )
    op.create_index(
        "ix_rule_set_audit_events_target_rule_set_id",
        "rule_set_audit_events",
        ["target_rule_set_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_rule_set_audit_events_target_rule_set_id",
        table_name="rule_set_audit_events",
    )
    op.drop_index(
        "ix_rule_set_audit_events_action",
        table_name="rule_set_audit_events",
    )
    op.drop_index(
        "ix_rule_set_audit_events_actor_subject",
        table_name="rule_set_audit_events",
    )
    op.drop_table("rule_set_audit_events")
