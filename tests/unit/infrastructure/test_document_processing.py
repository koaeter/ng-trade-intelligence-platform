from io import BytesIO

import pytest

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
    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R 5 0 R] /Count 2 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 300] /Resources << /Font << /F1 6 0 R >> >> /Contents 4 0 R >>",
        b"",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 300] /Resources << /Font << /F1 6 0 R >> >> /Contents 7 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"",
    ]
    streams = [
        b"BT /F1 12 Tf 20 250 Td (" + texts[0].encode("latin-1") + b") Tj ET",
        b"BT /F1 12 Tf 20 250 Td (" + texts[1].encode("latin-1") + b") Tj ET",
    ]
    objects[3] = b"<< /Length %d >>\nstream\n%s\nendstream" % (len(streams[0]), streams[0])
    objects[6] = b"<< /Length %d >>\nstream\n%s\nendstream" % (len(streams[1]), streams[1])

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f"{number} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")
    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    )
    return bytes(pdf)


def test_pdf_extractor_reads_pages_and_locations() -> None:
    data = make_pdf("Nigeria trade", "Second page")
    result = PypdfDocumentExtractor().extract(
        artifact(ArtifactKind.PDF), BytesIO(data), ExtractionPolicy()
    )
    assert result.page_count == 2
    assert result.artifact_id == "artifact-1"
    assert result.fragments[0].page_number == 1
    assert result.fragments[0].text == "Nigeria trade"
    assert result.fragments[1].locator == "page=2"


def test_pdf_page_limit_is_enforced() -> None:
    data = make_pdf("one", "two")
    with pytest.raises(ValueError, match="page limit"):
        PypdfDocumentExtractor().extract(
            artifact(ArtifactKind.PDF), BytesIO(data), ExtractionPolicy(max_pages=1)
        )


def test_pdf_output_limit_is_enforced() -> None:
    data = make_pdf("long text", "second")
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
        Store(make_pdf("PDF content", "page two")),
        [PypdfDocumentExtractor(), HtmlDocumentExtractor()],
    ).extract(artifact(ArtifactKind.PDF))
    assert pdf_result.extractor == "pypdf-extractor"

    html_result = ExtractedTextService(
        Store(b"<p>HTML content</p>"), [PypdfDocumentExtractor(), HtmlDocumentExtractor()]
    ).extract(artifact(ArtifactKind.HTML))
    assert html_result.extractor == "stdlib-html-extractor"
