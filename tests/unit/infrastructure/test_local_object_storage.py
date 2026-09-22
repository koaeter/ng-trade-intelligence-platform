from io import BytesIO
from pathlib import Path
import pytest

from infrastructure.storage.local import LocalObjectStorage


def test_local_storage_round_trip(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)
    storage.put("source/document.pdf", BytesIO(b"document"), "application/pdf")
    assert storage.get("source/document.pdf").read() == b"document"


def test_local_storage_rejects_traversal(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)
    with pytest.raises(ValueError):
        storage.put("../escape.txt", BytesIO(b"x"))
