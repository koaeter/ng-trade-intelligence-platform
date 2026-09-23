from io import BytesIO

from packages.application.source.document_extraction import (
    ExtractionFragment, ExtractionPolicy, ExtractionResult,
)
from packages.domain.source.artifacts import ArtifactKind


class PDFExtractor:
    supported_kinds = frozenset({ArtifactKind.PDF})

    def extract(self, content: BytesIO, policy: ExtractionPolicy) -> ExtractionResult:
        data = content.read(policy.max_input_bytes + 1)
        if len(data) > policy.max_input_bytes:
            raise ValueError("Source artifact exceeds configured input limit")
        try:
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(data), strict=False)
            page_count = len(reader.pages)
            if page_count > policy.max_pages:
                raise ValueError("PDF exceeds configured page limit")
            fragments: list[ExtractionFragment] = []
            for page_number, page in enumerate(reader.pages, 1):
                text = (page.extract_text() or "").strip()
                if text:
                    fragments.append(
                        ExtractionFragment(text, page_number=page_number, locator=f"page={page_number}")
                    )
            output = "\n\n".join(fragment.text for fragment in fragments)
            if len(output) > policy.max_output_characters:
                raise ValueError("Extracted text exceeds configured maximum")
            return ExtractionResult(
                "", output, "pypdf-extractor", "1", False, page_count, tuple(fragments)
            )
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError("PDF extraction failed") from exc
