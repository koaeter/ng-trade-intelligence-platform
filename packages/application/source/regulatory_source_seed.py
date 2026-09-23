from packages.domain.source.models import Source


# Initial corpus registrations based on current official public authority pages.
# These are source registrations only: acquisition, extraction, review and
# publication remain separate lifecycle stages.
INITIAL_NIGERIAN_REGULATORY_SOURCES = (
    Source("nepc-export-documents", "NEPC Export Documents & Procedures", "NEPC", "OFFICIAL_PROCEDURE", "ng", "https://nepc.gov.ng/get-started/export-documents-procedures/", endpoint_id="nepc-documents"),
    Source("nepc-e-registration", "NEPC Exporter E-registration", "NEPC", "OFFICIAL_SERVICE_GUIDANCE", "ng", "https://nepc.gov.ng/ereg/exporter", endpoint_id="nepc-eregistration"),
    Source("son-standards", "SON Standards", "SON", "OFFICIAL_STANDARDS_INFORMATION", "ng", "https://son.gov.ng/standards/", endpoint_id="son-standards"),
    Source("son-product-certification", "SON International Product Certification", "SON", "OFFICIAL_CERTIFICATION_GUIDANCE", "ng", "https://son.gov.ng/son-product-certification/", endpoint_id="son-home"),
    Source("nafdac-export-e-license", "NAFDAC Guidelines for Issuance of Export E-Licenses", "NAFDAC", "OFFICIAL_GUIDELINE", "ng", "https://nafdac.gov.ng/wp-content/uploads/Files/Resources/Guidelines/PORTINSPECTION_GUIDELINES/2022_To_2027/Guidelines-for-Issuance-of-Export-E-Licenses-for-NAFDAC-Regulated-Products.pdf", endpoint_id="nafdac-home"),
    Source("nafdac-food-export-health-certificate", "NAFDAC Health Certificate Guidelines for Processed and Semi-Processed Food Exports", "NAFDAC", "OFFICIAL_GUIDELINE", "ng", "https://www.nafdac.gov.ng/wp-content/uploads/Files/Resources/Guidelines/PORTINSPECTION_GUIDELINES/Guidelines-for-the-Issuance-of-Health-Certificate-for-Exportation-of-Processed-and-Semi-Processed-Food-Commodities.pdf", endpoint_id="nafdac-home"),
    Source("naqs-export-requirements", "NAQS Export Requirements", "NAQS", "OFFICIAL_EXPORT_REQUIREMENTS", "ng", "https://naqs.gov.ng/export-requirements/", endpoint_id="naqs-export-requirements"),
    Source("naqs-plant-quarantine", "NAQS Plant Quarantine", "NAQS", "OFFICIAL_REGULATORY_GUIDANCE", "ng", "https://naqs.gov.ng/plant_quarantine/", endpoint_id="naqs-home"),
    Source("ncs-export-procedure", "Nigeria Customs Service Export Procedure", "NCS", "OFFICIAL_EXPORT_PROCEDURE", "ng", "https://www.customs.gov.ng/rules-guidelines/export-procedure", endpoint_id="ncs-home"),
)
