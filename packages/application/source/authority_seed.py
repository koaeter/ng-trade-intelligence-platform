from packages.domain.source.authority_registry import Authority


INITIAL_NIGERIAN_AUTHORITIES = (
    Authority("nepc", "Nigerian Export Promotion Council", "NEPC", "ng", "EXPORT_PROMOTION", "https://nepc.gov.ng/"),
    Authority("ncs", "Nigeria Customs Service", "NCS", "ng", "CUSTOMS", "https://www.customs.gov.ng/"),
    Authority("son", "Standards Organisation of Nigeria", "SON", "ng", "STANDARDS", "https://son.gov.ng/"),
    Authority("nafdac", "National Agency for Food and Drug Administration and Control", "NAFDAC", "ng", "PRODUCT_REGULATION", "https://nafdac.gov.ng/"),
    Authority("naqs", "Nigeria Agricultural Quarantine Service", "NAQS", "ng", "PHYTOSANITARY", "https://naqs.gov.ng/"),
    Authority("dvcps", "Department of Veterinary and Pest Control Services", "DVPCS", "ng", "VETERINARY", None),
    Authority("fisheries", "Department of Fisheries", None, "ng", "FISHERIES", None),
    Authority("ninas", "Nigeria National Accreditation Service", "NiNAS", "ng", "ACCREDITATION", "https://ninas.ng/"),
)
