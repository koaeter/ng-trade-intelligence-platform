from io import BytesIO

from packages.application.source.content_validation import (
    ContentValidationService, DetectedArtifactFormat, ScanResult, ScanStatus,
)

class Scanner:
    def __init__(self, result):
        self.result = result
    def scan(self, content):
        return self.result

def validate(data, mime, status=ScanStatus.CLEAN):
    return ContentValidationService(Scanner(ScanResult(status))).validate(BytesIO(data), mime)

def test_valid_pdf():
    result = validate(b"%PDF-1.7\nbody", "application/pdf")
    assert result.accepted and result.detected_format == DetectedArtifactFormat.PDF

def test_valid_png():
    result = validate(b"\x89PNG\r\n\x1a\nbody", "image/png")
    assert result.accepted and result.detected_format == DetectedArtifactFormat.PNG

def test_valid_jpeg():
    result = validate(b"\xff\xd8\xffbody", "image/jpeg")
    assert result.accepted and result.detected_format == DetectedArtifactFormat.JPEG

def test_valid_docx_container():
    result = validate(b"PK\x03\x04office", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert result.accepted and result.detected_format == DetectedArtifactFormat.ZIP_CONTAINER

def test_mismatched_mime_rejected():
    result = validate(b"%PDF-1.7\nbody", "image/png")
    assert not result.accepted and "MIME" in (result.reason or "")

def test_infected_content_rejected():
    result = validate(b"%PDF-1.7\nbody", "application/pdf", ScanStatus.INFECTED)
    assert not result.accepted and result.scan_status == ScanStatus.INFECTED

def test_scanner_unavailable_rejected():
    result = validate(b"%PDF-1.7\nbody", "application/pdf", ScanStatus.UNAVAILABLE)
    assert not result.accepted and result.scan_status == ScanStatus.UNAVAILABLE

def test_scanner_error_rejected():
    result = validate(b"%PDF-1.7\nbody", "application/pdf", ScanStatus.ERROR)
    assert not result.accepted and result.scan_status == ScanStatus.ERROR

def test_unknown_signature_rejected():
    result = validate(b"\x00\x01\x02", "application/pdf")
    assert not result.accepted and result.detected_format == DetectedArtifactFormat.UNKNOWN

def test_html_is_text_like():
    result = validate(b"<!doctype html><html><body>x</body></html>", "text/html")
    assert result.accepted and result.detected_format == DetectedArtifactFormat.TEXT
