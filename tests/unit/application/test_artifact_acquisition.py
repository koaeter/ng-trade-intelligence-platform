from io import BytesIO
import pytest

from packages.application.source.artifact_acquisition import ArtifactAcquisitionPolicy, ArtifactAcquisitionService
from packages.application.source.content_validation import ContentValidationService, ScanResult, ScanStatus
from packages.application.source.object_storage import StoredObject

class Store:
    def __init__(self):
        self.objects = {}
    def put(self, key, content, content_type=None):
        data = content.read()
        self.objects[key] = data
        return StoredObject(key, content_type, len(data))

class Scanner:
    def __init__(self, status=ScanStatus.CLEAN):
        self.status = status
    def scan(self, content):
        return ScanResult(self.status)

def service(store, status=ScanStatus.CLEAN):
    return ArtifactAcquisitionService(
        store,
        validator=ContentValidationService(Scanner(status)),
    )

def test_acquisition_calculates_checksum_and_stores_content():
    store = Store()
    data = b"%PDF-1.7\nhello"
    result = service(store).acquire("source-1/doc-1.pdf", BytesIO(data), "application/pdf")
    assert result.size_bytes == len(data)
    assert store.objects["source-1/doc-1.pdf"] == data

def test_acquisition_rejects_unsupported_mime_type():
    with pytest.raises(ValueError, match="Unsupported content type"):
        service(Store()).acquire("doc.exe", BytesIO(b"bad"), "application/x-msdownload")

def test_acquisition_rejects_oversized_content():
    service_instance = service(Store())
    service_instance.policy = ArtifactAcquisitionPolicy(max_size_bytes=4)
    with pytest.raises(ValueError, match="maximum size"):
        service_instance.acquire("doc.pdf", BytesIO(b"12345"), "application/pdf")

def test_acquisition_rejects_path_traversal():
    with pytest.raises(ValueError, match="traversal"):
        service(Store()).acquire("../doc.pdf", BytesIO(b"data"), "application/pdf")

def test_acquisition_does_not_store_when_content_validation_fails():
    store = Store()
    with pytest.raises(ValueError, match="validation|MIME"):
        service(store).acquire("doc.pdf", BytesIO(b"not-a-pdf"), "application/pdf")
    assert store.objects == {}

def test_acquisition_rejects_infected_content_before_storage():
    store = Store()
    with pytest.raises(ValueError):
        service(store, ScanStatus.INFECTED).acquire("doc.pdf", BytesIO(b"%PDF-1.7\nbody"), "application/pdf")
    assert store.objects == {}

def test_acquisition_rejects_unavailable_scanner_before_storage():
    store = Store()
    with pytest.raises(ValueError):
        service(store, ScanStatus.UNAVAILABLE).acquire("doc.pdf", BytesIO(b"%PDF-1.7\nbody"), "application/pdf")
    assert store.objects == {}
