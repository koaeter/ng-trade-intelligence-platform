from io import BytesIO
import pytest

from packages.application.source.artifact_acquisition import ArtifactAcquisitionPolicy, ArtifactAcquisitionService
from packages.application.source.object_storage import StoredObject


class Store:
    def __init__(self):
        self.objects = {}

    def put(self, key, content, content_type=None):
        data = content.read()
        self.objects[key] = data
        return StoredObject(key, content_type, len(data))


def test_acquisition_calculates_checksum_and_stores_content():
    store = Store()
    result = ArtifactAcquisitionService(store).acquire("source-1/doc-1.pdf", BytesIO(b"hello"), "application/pdf")
    assert result.size_bytes == 5
    assert result.checksum_sha256 == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    assert store.objects["source-1/doc-1.pdf"] == b"hello"


def test_acquisition_rejects_unsupported_mime_type():
    with pytest.raises(ValueError, match="Unsupported content type"):
        ArtifactAcquisitionService(Store()).acquire("doc.exe", BytesIO(b"bad"), "application/x-msdownload")


def test_acquisition_rejects_oversized_content():
    service = ArtifactAcquisitionService(Store(), ArtifactAcquisitionPolicy(max_size_bytes=4))
    with pytest.raises(ValueError, match="maximum size"):
        service.acquire("doc.pdf", BytesIO(b"12345"), "application/pdf")


def test_acquisition_rejects_path_traversal():
    with pytest.raises(ValueError, match="traversal"):
        ArtifactAcquisitionService(Store()).acquire("../doc.pdf", BytesIO(b"data"), "application/pdf")
