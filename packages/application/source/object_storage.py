from dataclasses import dataclass
from typing import BinaryIO, Protocol


@dataclass(frozen=True)
class StoredObject:
    key: str
    content_type: str | None = None
    size_bytes: int | None = None


class ObjectStorage(Protocol):
    """Provider-neutral boundary for binary source artifacts."""

    def put(self, key: str, content: BinaryIO, content_type: str | None = None) -> StoredObject: ...

    def get(self, key: str) -> BinaryIO: ...

    def delete(self, key: str) -> None: ...
