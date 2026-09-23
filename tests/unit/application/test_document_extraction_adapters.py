from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from infrastructure.extraction.html import HTMLExtractor
from infrastructure.extraction.ooxml import DOCXExtractor
from infrastructure.extraction.security import validate_zip_container
from packages.application.source.document_extraction import ExtractionPolicy


def test_html_extractor_removes_active_content_and_preserves_text():
    result = HTMLExtractor().extract(
        BytesIO(b"<html><script>alert(1)</script><h1>Title</h1><p>Requirement text.</p></html>"),
        ExtractionPolicy(),
    )
    assert "alert" not in result.text
    assert "Requirement text." in result.text
    assert result.fragments


def test_docx_extractor_reads_paragraphs():
    xml = b'''<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body><w:p><w:r><w:t>Certificate required.</w:t></w:r></w:p></w:body></w:document>'''
    payload = BytesIO()
    with ZipFile(payload, "w", ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", xml)
    result = DOCXExtractor().extract(BytesIO(payload.getvalue()), ExtractionPolicy())
    assert result.text == "Certificate required."
    assert result.fragments[0].locator == "paragraph=1"


def test_zip_path_traversal_is_rejected():
    payload = BytesIO()
    with ZipFile(payload, "w", ZIP_DEFLATED) as archive:
        archive.writestr("../evil.txt", "x")
    with ZipFile(BytesIO(payload.getvalue())) as archive:
        with pytest.raises(ValueError, match="unsafe"):
            validate_zip_container(archive, ExtractionPolicy())


def test_zip_member_limit_is_enforced():
    payload = BytesIO()
    with ZipFile(payload, "w", ZIP_DEFLATED) as archive:
        archive.writestr("one.txt", "x")
    with ZipFile(BytesIO(payload.getvalue())) as archive:
        with pytest.raises(ValueError, match="too many"):
            validate_zip_container(archive, ExtractionPolicy(max_zip_members=0))
