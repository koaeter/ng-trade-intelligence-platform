# Pass 79 — Authority Source Endpoints

## Purpose

Pass 79 creates a governed endpoint catalogue underneath the authority registry.

The distinction is:

- Authority = who the institution is.
- Endpoint = where the institution publishes information.
- Source = a specific information source acquired/classified from an endpoint.
- Document/artifact = the concrete captured publication.
- Provision/requirement = reviewed structured knowledge derived from it.

This prevents an authority's homepage from being treated as if it were itself a single legal source.

## Endpoint model

    Authority
       |
       +-- AuthorityEndpoint
              |
              v
           Source
              |
              v
        Document / Artifact
              |
              v
        Provision / Requirement

Endpoint metadata includes endpoint type, access method, content format and purpose.

## Initial catalogue

The first Nigerian endpoint seed covers NEPC, NCS, SON, NAFDAC, NAQS and NiNAS, with additional targeted endpoints for NEPC export documentation/e-registration and SON standards.

The endpoints are public official web locations. They are discovery/acquisition targets, not automatic legal authorities. Every acquired source still enters the source lifecycle and review process.

Current official pages support the endpoint classifications: NEPC publishes export documents/procedures and its exporter e-registration service; NCS operates the official customs portal; SON publishes standards information; NAQS publishes import/export requirements and quarantine services. citeturn0search1turn0search2turn1search4turn1search2turn1search0

## Next dependency

The next pass can introduce source registration from an endpoint, including retrieval metadata and source-to-endpoint provenance, without yet publishing regulatory knowledge.
