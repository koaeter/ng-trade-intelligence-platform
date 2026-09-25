from html.parser import HTMLParser
from typing import BinaryIO

from packages.application.source.document_extraction import (
    ExtractionFragment,
    ExtractionPolicy,
    ExtractionResult,
)
from packages.domain.source.artifacts import ArtifactKind, SourceArtifact


class _VisibleTextParser(HTMLParser):
    """Extracts visible text without executing HTML content."""

    _ignored = frozenset({"script", "style", "noscript", "template"})
    _headings = frozenset({"h1", "h2", "h3", "h4", "h5", "h6"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._ignored_depth = 0
        self._heading: str | None = None
        self.title = ""
        self.fragments: list[ExtractionFragment] = []
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag in self._ignored:
            self._ignored_depth += 1
        elif tag == "title":
            self._heading = "title"
        elif tag in self._headings:
            self._heading = tag

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self._ignored and self._ignored_depth:
            self._ignored_depth -= 1
            return
        if self._heading is not None and tag in {"title", *self._headings}:
            value = " ".join(" ".join(self._buffer).split())
            if value:
                if self._heading == "title":
                    self.title = value
                else:
                    self.fragments.append(
                        ExtractionFragment(value, section=self._heading)
                    )
            self._buffer.clear()
            self._heading = None

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        value = " ".join(data.split())
        if not value:
            return
        if self._heading is not None:
            self._buffer.append(value)
        else:
            self.fragments.append(ExtractionFragment(value))

    def error(self, message: str) -> None:
        raise ValueError(f"Malformed HTML: {message}")


class HtmlDocumentExtractor:
    """Parses HTML locally; scripts/styles are data, never executable code."""

    supported_kinds = frozenset({ArtifactKind.HTML})
    name = "stdlib-html-extractor"
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
            html = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("HTML artifact is not valid UTF-8") from exc

        parser = _VisibleTextParser()
        try:
            parser.feed(html)
            parser.close()
        except Exception as exc:
            raise ValueError("HTML could not be parsed safely") from exc

        fragments = tuple(parser.fragments)
        text = "\n".join(fragment.text for fragment in fragments)
        if len(text) > policy.max_output_characters:
            raise ValueError("Extracted text exceeds configured maximum")

        if parser.title:
            fragments = (
                (ExtractionFragment(parser.title, section="title"),) + fragments
            )
            text = "\n".join(fragment.text for fragment in fragments)
            if len(text) > policy.max_output_characters:
                raise ValueError("Extracted text exceeds configured maximum")

        return ExtractionResult(
            artifact_id=artifact.id,
            text=text,
            extractor=self.name,
            extractor_version=self.version,
            ocr_used=False,
            page_count=None,
            fragments=fragments,
        )
