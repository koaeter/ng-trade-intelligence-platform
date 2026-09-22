from packages.domain.source.artifacts import ArtifactProcessingState, ExtractedText, SourceArtifact


class DocumentArtifactService:
    """Coordinates acquisition/extraction without making extracted text authoritative."""

    def __init__(self, artifacts, extracted_text):
        self.artifacts = artifacts
        self.extracted_text = extracted_text

    def register_acquired_artifact(self, artifact: SourceArtifact) -> SourceArtifact:
        if artifact.processing_state != ArtifactProcessingState.ACQUIRED:
            raise ValueError("Newly registered artifact must start in ACQUIRED state")
        self.artifacts.add(artifact)
        return artifact

    def record_extraction(self, artifact: SourceArtifact, extracted: ExtractedText) -> ExtractedText:
        if extracted.artifact_id != artifact.id:
            raise ValueError("Extracted text must reference its artifact")
        self.extracted_text.add(extracted)
        return extracted
