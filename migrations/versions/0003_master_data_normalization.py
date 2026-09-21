"""normalize governed master data and scenario references"""
from alembic import op
import sqlalchemy as sa
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column("export_scenarios", sa.Column("hs_version_id", sa.String(64), nullable=True))
    op.create_foreign_key("fk_scenario_product", "export_scenarios", "products", ["product_id"], ["id"])
    op.create_foreign_key("fk_scenario_origin", "export_scenarios", "countries", ["origin_country_code"], ["code"])
    op.create_foreign_key("fk_scenario_market", "export_scenarios", "markets", ["destination_market_code"], ["code"])
    op.create_table("requirement_products",
        sa.Column("requirement_id", sa.String(64), sa.ForeignKey("requirements.id"), primary_key=True),
        sa.Column("product_id", sa.String(64), sa.ForeignKey("products.id"), primary_key=True))
    op.create_table("requirement_hs_codes",
        sa.Column("requirement_id", sa.String(64), sa.ForeignKey("requirements.id"), primary_key=True),
        sa.Column("hs_version_id", sa.String(64), primary_key=True),
        sa.Column("hs_code", sa.String(32), primary_key=True))
    op.create_table("requirement_origin_countries",
        sa.Column("requirement_id", sa.String(64), sa.ForeignKey("requirements.id"), primary_key=True),
        sa.Column("country_code", sa.String(2), sa.ForeignKey("countries.code"), primary_key=True))
    op.create_table("requirement_destination_markets",
        sa.Column("requirement_id", sa.String(64), sa.ForeignKey("requirements.id"), primary_key=True),
        sa.Column("market_code", sa.String(64), sa.ForeignKey("markets.code"), primary_key=True))
    op.create_table("requirement_evidence",
        sa.Column("requirement_id", sa.String(64), sa.ForeignKey("requirements.id"), primary_key=True),
        sa.Column("evidence_id", sa.String(64), sa.ForeignKey("evidence.id"), primary_key=True))

def downgrade() -> None:
    op.drop_table("requirement_evidence")
    op.drop_table("requirement_destination_markets")
    op.drop_table("requirement_origin_countries")
    op.drop_table("requirement_hs_codes")
    op.drop_table("requirement_products")
    op.drop_constraint("fk_scenario_market", "export_scenarios", type_="foreignkey")
    op.drop_constraint("fk_scenario_origin", "export_scenarios", type_="foreignkey")
    op.drop_constraint("fk_scenario_product", "export_scenarios", type_="foreignkey")
    op.drop_column("export_scenarios", "hs_version_id")
