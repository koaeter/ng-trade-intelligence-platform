from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
from typing import BinaryIO

from packages.application.source.object_storage import ObjectStorage


@dataclass(frozen=True)
class ArtifactAcquisitionPolicy:
    max_size_bytes: int = 25 * 1024 * 1024
    allowed_mime_types: frozenset[str] = frozenset({
        "application/pdf", "text/html", "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/csv", "image/jpeg", "image/png",
    })


@dataclass(frozen=True)
class AcquiredObject:
    storage_key: str
    checksum_sha256: str
    size_bytes: int
    content_type: str | None


class ArtifactAcquisitionService:
    """Validates bounded source content and stores it through the storage port."""

    def __init__(self, storage: ObjectStorage, policy: ArtifactAcquisitionPolicy | None = None) -> None:
        self.storage = storage
        self.policy = policy or ArtifactAcquisitionPolicy()

    def acquire(self, key: str, content: BinaryIO, content_type: str | None = None) -> AcquiredObject:
        if not key or key.startswith("/") or ".." in key.split("/"):
            raise ValueError("Storage key must be a relative, traversal-safe path")
        if content_type is not None and content_type not in self.policy.allowed_mime_types:
            raise ValueError(f"Unsupported content type: {content_type}")

        digest = sha256()
        chunks: list[bytes] = []
        size = 0
        while True:
            chunk = content.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > self.policy.max_size_bytes:
                raise ValueError("Artifact exceeds configured maximum size")
            digest.update(chunk)
            chunks.append(chunk)

        stored = self.storage.put(key, BytesIO(b"".join(chunks)), content_type)
        if stored.key != key:
            raise ValueError("Object storage returned a different storage key")
        if stored.size_bytes is not None and stored.size_bytes != size:
            raise ValueError("Stored object size does not match acquired content")
        return AcquiredObject(key, digest.hexdigest(), size, content_type)
