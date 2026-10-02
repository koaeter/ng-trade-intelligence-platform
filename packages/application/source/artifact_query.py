from packages.application.source.artifact_repositories import SourceArtifactRepository
from packages.domain.source.artifacts import SourceArtifact


class GetSourceArtifact:
    """Read one immutable acquired source artifact."""

    def __init__(self, artifacts: SourceArtifactRepository) -> None:
        self.artifacts = artifacts

    def execute(self, artifact_id: str) -> SourceArtifact:
        artifact = self.artifacts.get(artifact_id)
        if artifact is None:
            raise ValueError("Source artifact does not exist")
        return artifact
