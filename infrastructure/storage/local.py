from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from packages.application.source.object_storage import StoredObject


class LocalObjectStorage:
    """Development object storage; production adapters should target managed/object storage."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        if not key or key.startswith("/") or ".." in key.split("/"):
            raise ValueError("Storage key must be relative and traversal-safe")
        path = (self.root / key).resolve()
        if self.root != path and self.root not in path.parents:
            raise ValueError("Storage key escapes storage root")
        return path

    def put(self, key: str, content: BinaryIO, content_type: str | None = None) -> StoredObject:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = content.read()
        path.write_bytes(data)
        return StoredObject(key, content_type, len(data))

    def get(self, key: str) -> BinaryIO:
        return BytesIO(self._path(key).read_bytes())

    def delete(self, key: str) -> None:
        path = self._path(key)
        if path.exists():
            path.unlink()
