from io import BytesIO
from typing import BinaryIO

from pypdf import PdfReader

from packages.application.source.document_extraction import (
    ExtractionFragment,
    ExtractionPolicy,
    ExtractionResult,
)
from packages.domain.source.artifacts import ArtifactKind, SourceArtifact


class PypdfDocumentExtractor:
    """Page-aware PDF extraction with bounded pages and output."""

    supported_kinds = frozenset({ArtifactKind.PDF})
    name = "pypdf-extractor"
    version = "1"

    def extract(
        self,
        artifact: SourceArtifact,
        content: BinaryIO,
        policy: ExtractionPolicy,
    ) -> ExtractionResult:
        data = content.read(policy.max_input_bytes + 1)
        if len(data) > policy.max_input_bytes:
            raise ValueError("Source artifact exceeds configured input limit")

        try:
            reader = PdfReader(BytesIO(data), strict=True)
        except Exception as exc:
            raise ValueError("PDF could not be parsed safely") from exc

        page_count = len(reader.pages)
        if page_count > policy.max_pages:
            raise ValueError("PDF exceeds configured page limit")

        fragments: list[ExtractionFragment] = []
        pages: list[str] = []
        total = 0

        for number, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:
                raise ValueError(f"PDF page {number} could not be extracted") from exc

            text = text.strip()
            if not text:
                continue

            remaining = policy.max_output_characters - total
            if remaining <= 0:
                raise ValueError("Extracted text exceeds configured maximum")
            if len(text) > remaining:
                raise ValueError("Extracted text exceeds configured maximum")

            fragments.append(
                ExtractionFragment(
                    text=text,
                    page_number=number,
                    locator=f"page={number}",
                )
            )
            pages.append(text)
            total += len(text)

        return ExtractionResult(
            artifact_id=artifact.id,
            text="\n\n".join(pages),
            extractor=self.name,
            extractor_version=self.version,
            ocr_used=False,
            page_count=page_count,
            fragments=tuple(fragments),
        )
