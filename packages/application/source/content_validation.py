from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import BinaryIO, Protocol

class DetectedArtifactFormat(str, Enum):
    PDF = "PDF"
    PNG = "PNG"
    JPEG = "JPEG"
    ZIP_CONTAINER = "ZIP_CONTAINER"
    TEXT = "TEXT"
    UNKNOWN = "UNKNOWN"

class ScanStatus(str, Enum):
    CLEAN = "CLEAN"
    INFECTED = "INFECTED"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"

@dataclass(frozen=True)
class ScanResult:
    status: ScanStatus
    reason: str | None = None

class MalwareScanner(Protocol):
    def scan(self, content: BinaryIO) -> ScanResult: ...

class NoOpMalwareScanner:
    """Development boundary only; it does not provide malware protection."""
    def scan(self, content: BinaryIO) -> ScanResult:
        return ScanResult(ScanStatus.UNAVAILABLE, "No malware scanner is configured")

@dataclass(frozen=True)
class ContentValidationResult:
    detected_format: DetectedArtifactFormat
    declared_mime_type: str | None
    scan_status: ScanStatus
    accepted: bool
    reason: str | None = None

class ContentValidationService:
    MIME_BY_FORMAT = {
        DetectedArtifactFormat.PDF: frozenset({"application/pdf"}),
        DetectedArtifactFormat.PNG: frozenset({"image/png"}),
        DetectedArtifactFormat.JPEG: frozenset({"image/jpeg"}),
        DetectedArtifactFormat.ZIP_CONTAINER: frozenset({
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }),
        DetectedArtifactFormat.TEXT: frozenset({"text/plain", "text/html", "text/csv"}),
    }

    def __init__(self, scanner: MalwareScanner) -> None:
        self.scanner = scanner

    def validate(self, content: BinaryIO, declared_mime_type: str | None) -> ContentValidationResult:
        data = content.read()
        detected = self._detect(data)
        if declared_mime_type is not None and declared_mime_type not in self.MIME_BY_FORMAT.get(detected, frozenset()):
            return ContentValidationResult(detected, declared_mime_type, ScanStatus.ERROR, False, "Declared MIME type does not match detected content format")
        scan = self.scanner.scan(BytesIO(data))
        if scan.status != ScanStatus.CLEAN:
            return ContentValidationResult(detected, declared_mime_type, scan.status, False, scan.reason)
        if detected == DetectedArtifactFormat.UNKNOWN:
            return ContentValidationResult(detected, declared_mime_type, scan.status, False, "Unknown content format")
        return ContentValidationResult(detected, declared_mime_type, scan.status, True)

    @staticmethod
    def _detect(data: bytes) -> DetectedArtifactFormat:
        if data.startswith(b"%PDF-"):
            return DetectedArtifactFormat.PDF
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            return DetectedArtifactFormat.PNG
        if data.startswith(b"\xff\xd8\xff"):
            return DetectedArtifactFormat.JPEG
        if data.startswith(b"PK\x03\x04"):
            return DetectedArtifactFormat.ZIP_CONTAINER
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            return DetectedArtifactFormat.UNKNOWN
        if "<html" in text[:4096].lower() or "<!doctype html" in text[:4096].lower():
            return DetectedArtifactFormat.TEXT
        if data.strip():
            return DetectedArtifactFormat.TEXT
        return DetectedArtifactFormat.UNKNOWN
