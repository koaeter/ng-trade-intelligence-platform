from datetime import date

from packages.domain.source.models import Document


# Document metadata is intentionally separate from the source URL. The source
# identifies the authority publication location; the document identifies the
# individual regulatory/procedural item that must later be acquired and reviewed.
INITIAL_NIGERIAN_DOCUMENTS = (
    Document("doc-nepc-export-documents", "nepc-export-documents", "NEPC Export Documents & Procedures", "PROCEDURE_GUIDANCE"),
    Document("doc-nepc-e-registration", "nepc-e-registration", "NEPC Exporter E-registration", "SERVICE_GUIDANCE"),
    Document("doc-son-standards", "son-standards", "SON Standards", "STANDARDS_INFORMATION"),
    Document("doc-son-product-certification", "son-product-certification", "SON International Product Certification", "CERTIFICATION_GUIDANCE"),
    Document("doc-nafdac-export-e-license", "nafdac-export-e-license", "Guidelines for Issuance of Export E-Licenses for NAFDAC Regulated Products", "GUIDELINE", effective_from=date(2022, 9, 24), effective_to=date(2027, 9, 23), version_label="PID-GDL-011-00"),
    Document("doc-nafdac-food-health-certificate", "nafdac-food-export-health-certificate", "Guidelines for the Issuance of Health Certificate for Exportation of Processed and Semi-Processed Food Commodities", "GUIDELINE", effective_from=date(2018, 6, 1), version_label="PID-GDL-013-00"),
    Document("doc-naqs-export-requirements", "naqs-export-requirements", "NAQS Export Requirements", "EXPORT_REQUIREMENTS"),
    Document("doc-naqs-plant-quarantine", "naqs-plant-quarantine", "NAQS Plant Quarantine", "REGULATORY_GUIDANCE"),
    Document("doc-ncs-export-procedure", "ncs-export-procedure", "Nigeria Customs Service Export Procedure", "EXPORT_PROCEDURE"),
)
