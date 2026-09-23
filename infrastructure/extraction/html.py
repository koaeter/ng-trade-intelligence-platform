from io import BytesIO
from html.parser import HTMLParser

from packages.application.source.document_extraction import (
    ExtractionFragment, ExtractionPolicy, ExtractionResult,
)
from packages.domain.source.artifacts import ArtifactKind


class _SafeHTMLParser(HTMLParser):
    _ignored = {"script", "style", "noscript", "template", "svg", "canvas"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.fragments: list[ExtractionFragment] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in self._ignored:
            self.ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self._ignored and self.ignored_depth:
            self.ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.ignored_depth:
            return
        value = " ".join(data.split())
        if value:
            self.parts.append(value)

    def close(self) -> None:
        super().close()
        self.fragments = tuple(
            ExtractionFragment(value, locator=f"html-node={index}")
            for index, value in enumerate(self.parts, 1)
        )


class HTMLExtractor:
    supported_kinds = frozenset({ArtifactKind.HTML})

    def extract(self, content: BytesIO, policy: ExtractionPolicy) -> ExtractionResult:
        data = content.read(policy.max_input_bytes + 1)
        if len(data) > policy.max_input_bytes:
            raise ValueError("Source artifact exceeds configured input limit")
        try:
            parser = _SafeHTMLParser()
            parser.feed(data.decode("utf-8"))
            parser.close()
        except UnicodeDecodeError as exc:
            raise ValueError("HTML artifact is not valid UTF-8") from exc
        except Exception as exc:
            raise ValueError("HTML extraction failed") from exc
        text = "\n".join(fragment.text for fragment in parser.fragments)
        if len(text) > policy.max_output_characters:
            raise ValueError("Extracted text exceeds configured maximum")
        return ExtractionResult("", text, "safe-html-extractor", "1", False, None, tuple(parser.fragments))
