from pathlib import PurePosixPath
from zipfile import ZipFile

from packages.application.source.document_extraction import ExtractionPolicy


def validate_zip_container(archive: ZipFile, policy: ExtractionPolicy) -> None:
    infos = archive.infolist()
    if len(infos) > policy.max_zip_members:
        raise ValueError("Archive contains too many members")
    total = 0
    for info in infos:
        name = PurePosixPath(info.filename)
        if info.filename.startswith("/") or ".." in name.parts:
            raise ValueError("Archive contains an unsafe path")
        if info.file_size > policy.max_zip_member_bytes:
            raise ValueError("Archive member exceeds configured limit")
        total += info.file_size
        if total > policy.max_zip_uncompressed_bytes:
            raise ValueError("Archive uncompressed size exceeds configured limit")
