from packages.domain.source.authority_endpoint import AuthorityEndpoint


# Official endpoints verified against the authorities' current public websites.
# Endpoint registration does not imply that every item reachable at the URL is
# a legally authoritative instrument; individual sources still require
# acquisition, classification, review and publication.
INITIAL_NIGERIAN_AUTHORITY_ENDPOINTS = (
    AuthorityEndpoint("nepc-home", "nepc", "https://nepc.gov.ng/", "OFFICIAL_PORTAL", purpose="Official NEPC portal."),
    AuthorityEndpoint("nepc-documents", "nepc", "https://nepc.gov.ng/get-started/export-documents-procedures/", "EXPORT_PROCEDURES", purpose="Export documents and procedures."),
    AuthorityEndpoint("nepc-eregistration", "nepc", "https://nepc.gov.ng/ereg/exporter", "SERVICE_PORTAL", purpose="Exporter e-registration service."),
    AuthorityEndpoint("ncs-home", "ncs", "https://www.customs.gov.ng/", "OFFICIAL_PORTAL", purpose="Official NCS portal and trade information."),
    AuthorityEndpoint("son-home", "son", "https://son.gov.ng/", "OFFICIAL_PORTAL", purpose="Official SON portal."),
    AuthorityEndpoint("son-standards", "son", "https://son.gov.ng/standards/", "STANDARDS_CATALOGUE", purpose="Public standards information."),
    AuthorityEndpoint("nafdac-home", "nafdac", "https://www.nafdac.gov.ng/", "OFFICIAL_PORTAL", purpose="Official NAFDAC portal."),
    AuthorityEndpoint("naqs-home", "naqs", "https://www.naqs.gov.ng/", "OFFICIAL_PORTAL", purpose="Official NAQS portal."),
    AuthorityEndpoint("naqs-export-requirements", "naqs", "https://naqs.gov.ng/", "EXPORT_REQUIREMENTS", purpose="Official portal containing import/export requirements and quarantine services."),
    AuthorityEndpoint("ninas-home", "ninas", "https://ninas.ng/", "OFFICIAL_PORTAL", purpose="Official NiNAS portal."),
)
