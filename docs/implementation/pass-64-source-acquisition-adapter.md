# Pass 64 — Source acquisition adapter

## Objective

Add a concrete, bounded external-source fetcher without allowing arbitrary URLs to become an SSRF-capable ingestion path.

## Implemented

- Provider-neutral SourceFetcher application port.
- HTTPS-only acquisition.
- Explicit hostname allowlist.
- URL credential rejection.
- Private/loopback IP rejection.
- Maximum response-size enforcement.
- Request timeout.
- Explicit user agent.
- Automatic redirect following disabled.

## Security boundary

The source registry must explicitly authorize a host before the fetcher will contact it.

The fetcher does not decide whether the content is legally authoritative. It only retrieves bytes from an approved acquisition endpoint.

## Important limitation

Hostname allowlisting alone is not a complete production SSRF defence against DNS rebinding or malicious DNS infrastructure. A production deployment should perform network egress controls and resolve/validate destination addresses at the network boundary.

## Next

The next pass should connect successful source acquisition to SourceArtifact creation, checksum calculation and source lifecycle transitions.
