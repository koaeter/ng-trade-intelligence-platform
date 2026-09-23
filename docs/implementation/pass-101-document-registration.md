# Pass 101 — Document registration boundary

The corpus now has a formal document-registration boundary beneath sources. A document must reference a source, have a title and document type, and cannot silently overwrite an existing document ID.

This keeps source identity separate from document identity: one registered source may yield multiple documents and later artifacts without collapsing their provenance.
