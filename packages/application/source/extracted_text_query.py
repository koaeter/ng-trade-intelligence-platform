from packages.application.source.artifact_repositories import ExtractedTextRepository
from packages.domain.source.artifacts import ExtractedText


class GetExtractedText:
    """Read immutable extracted text associated with an artifact."""

    def __init__(self, texts: ExtractedTextRepository) -> None:
        self.texts = texts

    def execute(self, artifact_id: str) -> ExtractedText:
        extracted = self.texts.get(artifact_id)
        if extracted is None:
            raise ValueError("Extracted text does not exist")
        return extracted
