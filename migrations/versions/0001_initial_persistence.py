from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_persistence"
down_revision: Union[str, Sequence[str], None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("export_scenarios",
        sa.Column("id", sa.String(64), nullable=False), sa.Column("product_id", sa.String(64), nullable=False),
        sa.Column("hs_code", sa.String(32), nullable=False), sa.Column("origin_country_code", sa.String(2), nullable=False),
        sa.Column("destination_market_code", sa.String(32), nullable=False), sa.Column("scenario_date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"))
    op.create_table("requirements",
        sa.Column("id", sa.String(64), nullable=False), sa.Column("name", sa.String(255), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=False), sa.Column("effective_to", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"))
    op.create_table("applicability_evaluations",
        sa.Column("id", sa.String(64), nullable=False), sa.Column("scenario_id", sa.String(64), nullable=False),
        sa.Column("result", sa.String(32), nullable=False), sa.Column("rule_set_version", sa.String(64), nullable=False),
        sa.PrimaryKeyConstraint("id"))
    op.create_index("ix_applicability_evaluations_scenario_id", "applicability_evaluations", ["scenario_id"])


def downgrade() -> None:
    op.drop_index("ix_applicability_evaluations_scenario_id", table_name="applicability_evaluations")
    op.drop_table("applicability_evaluations")
    op.drop_table("requirements")
    op.drop_table("export_scenarios")
