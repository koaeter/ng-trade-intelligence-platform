"""Register every SQLAlchemy model before tests create the shared metadata schema.

Production migrations own schema creation. Tests that use Base.metadata.create_all()
need all model modules imported so cross-module foreign keys can be resolved.
"""
from infrastructure.database import (
    authority_endpoint_models,
    authority_models,
    authority_registry_models,
    authority_scope_models,
    fact_type_models,
    jurisdiction_models,
    models,
    regulatory_domain_models,
)

# Keep explicit imports visible to linters and document the metadata registration.
__all__ = [
    "authority_endpoint_models",
    "authority_models",
    "authority_registry_models",
    "authority_scope_models",
    "fact_type_models",
    "jurisdiction_models",
    "models",
    "regulatory_domain_models",
]
