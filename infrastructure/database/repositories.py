from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import uuid4

from infrastructure.database.models import (
    ApplicabilityEvaluationModel, CountryModel, DocumentModel, EvidenceModel,
    ExportScenarioModel, ExtractedTextModel, HSCodeModel, MarketModel, ProductModel,
    ProvisionModel, RequirementDestinationMarketModel, RequirementEvidenceModel,
    RequirementHSCodeModel, RequirementModel, RequirementOriginCountryModel,
    RequirementProductModel, SourceArtifactModel, SourceModel,
)
from packages.application.catalog.repositories import CountryRepository, HSCodeRepository, MarketRepository, ProductRepository
from packages.application.scenarios.repositories import ApplicabilityEvaluationRepository, EvidenceRepository, ExportScenarioRepository, RequirementRepository
from packages.application.source.artifact_repositories import ExtractedTextRepository, SourceArtifactRepository
from packages.application.source.repositories import DocumentRepository, ProvisionRepository, SourceRepository
from packages.domain.catalog.models import Country, HSCode, Market, Product
from packages.domain.evidence.models import Evidence
from packages.domain.requirement.models import Requirement
from packages.domain.scenario.models import ApplicabilityEvaluation, EvaluationResult, ExportScenario
from packages.domain.source.artifacts import ArtifactKind, ArtifactProcessingState, ExtractedText, SourceArtifact
from packages.domain.source.models import Document, Provision, Source, SourceStatus

# Existing repositories remain unchanged below; artifact repositories are appended to keep
# the infrastructure boundary explicit.

