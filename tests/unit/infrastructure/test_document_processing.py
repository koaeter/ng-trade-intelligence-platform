from io import BytesIO

import pytest
from pypdf import PdfWriter

from infrastructure.document_processing.html import HtmlDocumentExtractor
from infrastructure.document_processing.pdf import PypdfDocumentExtractor
from packages.application.source.document_extraction import ExtractionPolicy, ExtractedTextService
from packages.domain.source.artifacts import ArtifactKind, SourceArtifact


def artifact(kind: ArtifactKind) -> SourceArtifact:
    from datetime import datetime, timezone
    return SourceArtifact(
        id="artifact-1", source_id="source-1", document_id="doc-1",
        kind=kind, storage_key="source/doc", checksum_sha256="abc",
        acquired_at=datetime.now(timezone.utc),
    )


class Store:
    def __init__(self, data: bytes) -> None:
        self.data = data

    def get(self, key: str) -> BytesIO:
        return BytesIO(self.data)


def make_pdf(*texts: str) -> bytes:
    writer = PdfWriter()
    for text in texts:
        page = writer.add_blank_page(width=300, height=300)
        page.merge_page(_text_page(text))
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def _text_page(text: str):
    writer = PdfWriter()
    page = writer.add_blank_page(width=300, height=300)
    page["/Contents"] = writer._add_object(
        b"BT /F1 12 Tf 20 250 Td (" + text.encode("latin-1") + b") Tj ET"
    )
    return page


def test_pdf_extractor_reads_pages_and_locations() -> None:
    data = make_pdf("Nigeria trade", "Second page")
    result = PypdfDocumentExtractor().extract(
        artifact(ArtifactKind.PDF), BytesIO(data), ExtractionPolicy()
    )
    assert result.page_count == 2
    assert result.artifact_id == "artifact-1"
    assert result.fragments[0].page_number == 1
    assert result.fragments[1].locator == "page=2"


def test_pdf_page_limit_is_enforced() -> None:
    data = make_pdf("one", "two")
    with pytest.raises(ValueError, match="page limit"):
        PypdfDocumentExtractor().extract(
            artifact(ArtifactKind.PDF), BytesIO(data), ExtractionPolicy(max_pages=1)
        )


def test_pdf_output_limit_is_enforced() -> None:
    data = make_pdf("long text")
    with pytest.raises(ValueError, match="maximum"):
        PypdfDocumentExtractor().extract(
            artifact(ArtifactKind.PDF), BytesIO(data), ExtractionPolicy(max_output_characters=2)
        )


def test_html_strips_script_and_style_and_keeps_headings() -> None:
    html = b"""<html><head><title>Trade Notice</title><style>secret()</style></head>
    <body><h1>Export Requirements</h1><p>Certificate required.</p>
    <script>alert('x')</script></body></html>"""
    result = HtmlDocumentExtractor().extract(
        artifact(ArtifactKind.HTML), BytesIO(html), ExtractionPolicy()
    )
    assert result.text == "Trade Notice\nExport Requirements\nCertificate required."
    assert "alert" not in result.text
    assert "secret" not in result.text
    assert result.fragments[1].section == "h1"


def test_html_output_limit_is_enforced() -> None:
    html = b"<html><body><p>abcdef</p></body></html>"
    with pytest.raises(ValueError, match="maximum"):
        HtmlDocumentExtractor().extract(
            artifact(ArtifactKind.HTML), BytesIO(html),
            ExtractionPolicy(max_output_characters=3),
        )


def test_extraction_service_routes_pdf_and_html_adapters() -> None:
    pdf_result = ExtractedTextService(
        Store(make_pdf("PDF content")), [PypdfDocumentExtractor(), HtmlDocumentExtractor()]
    ).extract(artifact(ArtifactKind.PDF))
    assert pdf_result.extractor == "pypdf-extractor"

    html_result = ExtractedTextService(
        Store(b"<p>HTML content</p>"), [PypdfDocumentExtractor(), HtmlDocumentExtractor()]
    ).extract(artifact(ArtifactKind.HTML))
    assert html_result.extractor == "stdlib-html-extractor"
