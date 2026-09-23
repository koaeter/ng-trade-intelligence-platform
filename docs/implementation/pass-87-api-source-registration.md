# Pass 87 — API source registration through authority endpoints

The source-creation API now requires an authority endpoint ID and uses the endpoint-aware registration application service. Clients cannot create an acquisition source with an arbitrary official URL through this API; the registered source inherits the endpoint URL and retains endpoint provenance.

This keeps the API aligned with the source model established in Passes 79–80.
