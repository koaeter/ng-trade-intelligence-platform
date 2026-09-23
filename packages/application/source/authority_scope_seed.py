from packages.domain.source.authority_scope import AuthorityScopeAssignment


# These are scope declarations, not precedence rankings. They identify which
# Nigerian authorities should be considered when a source is classified into a
# jurisdiction/domain/fact-type combination.
INITIAL_NIGERIAN_AUTHORITY_SCOPES = (
    AuthorityScopeAssignment("nepc-documentation", "nepc", "ng", "trade", "DOCUMENTATION", notes="Exporter registration and export-document guidance."),
    AuthorityScopeAssignment("nepc-procedure", "nepc", "ng", "trade", "PROCEDURE", notes="Export procedures and exporter-facing process guidance."),
    AuthorityScopeAssignment("nepc-market-access", "nepc", "ng", "market_access", "MARKET_ACCESS", notes="Export promotion and market-access support; not a substitute for destination authority requirements."),
    AuthorityScopeAssignment("ncs-customs", "ncs", "ng", "customs", "PROCEDURE", notes="Customs/export declaration and border procedures."),
    AuthorityScopeAssignment("ncs-tariff", "ncs", "ng", "tariffs", "TARIFF", notes="Customs tariff administration; tariff facts remain source-specific and versioned."),
    AuthorityScopeAssignment("son-standard", "son", "ng", "standards", "STANDARD", notes="National standards applicable to goods."),
    AuthorityScopeAssignment("son-conformity", "son", "ng", "standards", "CERTIFICATION", notes="Conformity-assessment and certification-related facts."),
    AuthorityScopeAssignment("nafdac-sps", "nafdac", "ng", "sps", "SPS_MEASURE", notes="Regulated-product health/safety controls and certificates."),
    AuthorityScopeAssignment("nafdac-certification", "nafdac", "ng", "product_regulation", "CERTIFICATION", notes="Health/export certificates for regulated products."),
    AuthorityScopeAssignment("nafdac-procedure", "nafdac", "ng", "product_regulation", "PROCEDURE", notes="Procedures for regulated-product export controls."),
    AuthorityScopeAssignment("naqs-sps", "naqs", "ng", "sps", "SPS_MEASURE", notes="Phytosanitary measures for agricultural exports."),
    AuthorityScopeAssignment("naqs-certification", "naqs", "ng", "sps", "CERTIFICATION", notes="Phytosanitary certification."),
    AuthorityScopeAssignment("dvpcs-sps", "dvcps", "ng", "sps", "SPS_MEASURE", notes="Veterinary controls for animals and animal products."),
    AuthorityScopeAssignment("dvpcs-certification", "dvcps", "ng", "sps", "CERTIFICATION", notes="International veterinary certification."),
    AuthorityScopeAssignment("fisheries-sps", "fisheries", "ng", "sps", "SPS_MEASURE", notes="Health controls for fish and fishery products."),
    AuthorityScopeAssignment("fisheries-certification", "fisheries", "ng", "sps", "CERTIFICATION", notes="Health certification for fish and fishery products."),
    AuthorityScopeAssignment("ninas-conformity", "ninas", "ng", "standards", "CERTIFICATION", notes="Accreditation of conformity-assessment infrastructure; NiNAS is not itself the product regulator."),
)
