from io import BytesIO
from zipfile import BadZipFile, ZipFile
from xml.etree import ElementTree as ET

from infrastructure.extraction.security import validate_zip_container
from packages.application.source.document_extraction import (
    ExtractionFragment, ExtractionPolicy, ExtractionResult,
)
from packages.domain.source.artifacts import ArtifactKind

_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_SS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _zip(data: bytes, policy: ExtractionPolicy) -> ZipFile:
    try:
        archive = ZipFile(BytesIO(data))
        validate_zip_container(archive, policy)
        return archive
    except (BadZipFile, ValueError) as exc:
        raise ValueError("Invalid or unsafe Office Open XML container") from exc


class DOCXExtractor:
    supported_kinds = frozenset({ArtifactKind.DOCX})

    def extract(self, content: BytesIO, policy: ExtractionPolicy) -> ExtractionResult:
        data = content.read(policy.max_input_bytes + 1)
        if len(data) > policy.max_input_bytes:
            raise ValueError("Source artifact exceeds configured input limit")
        with _zip(data, policy) as archive:
            try:
                root = ET.fromstring(archive.read("word/document.xml"))
            except Exception as exc:
                raise ValueError("DOCX document.xml is invalid") from exc
        paragraphs: list[ExtractionFragment] = []
        for paragraph in root.findall(f".//{{{_W}}}p"):
            text = "".join(node.text or "" for node in paragraph.findall(f".//{{{_W}}}t")).strip()
            if text:
                paragraphs.append(
                    ExtractionFragment(text, locator=f"paragraph={len(paragraphs)+1}")
                )
        output = "\n".join(x.text for x in paragraphs)
        if len(output) > policy.max_output_characters:
            raise ValueError("Extracted text exceeds configured maximum")
        return ExtractionResult(
            "", output, "ooxml-docx-extractor", "1", False, None, tuple(paragraphs)
        )


class XLSXExtractor:
    supported_kinds = frozenset({ArtifactKind.XLSX})

    def extract(self, content: BytesIO, policy: ExtractionPolicy) -> ExtractionResult:
        data = content.read(policy.max_input_bytes + 1)
        if len(data) > policy.max_input_bytes:
            raise ValueError("Source artifact exceeds configured input limit")
        with _zip(data, policy) as archive:
            try:
                shared: list[str] = []
                if "xl/sharedStrings.xml" in archive.namelist():
                    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
                    shared = [
                        "".join(node.text or "" for node in item.findall(f".//{{{_SS}}}t"))
                        for item in root.findall(f".//{{{_SS}}}si")
                    ]
                workbook = ET.fromstring(archive.read("xl/workbook.xml"))
                rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
                targets = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
                sheets = workbook.findall(f".//{{{_SS}}}sheet")
                fragments: list[ExtractionFragment] = []
                for sheet in sheets:
                    rid = sheet.attrib.get(f"{{{_REL}}}id")
                    target = targets.get(rid or "")
                    if not target:
                        continue
                    path = target.lstrip("/")
                    if not path.startswith("xl/"):
                        path = "xl/" + path
                    root = ET.fromstring(archive.read(path))
                    for row in root.findall(f".//{{{_SS}}}row"):
                        values = []
                        for cell in row.findall(f"{{{_SS}}}c"):
                            value = cell.find(f"{{{_SS}}}v")
                            if value is None or value.text is None:
                                continue
                            raw = value.text
                            if cell.attrib.get("t") == "s":
                                index = int(raw)
                                raw = shared[index] if index < len(shared) else ""
                            values.append(raw)
                        if values:
                            fragments.append(
                                ExtractionFragment(
                                    " | ".join(values),
                                    section=sheet.attrib.get("name"),
                                    locator=f"sheet={sheet.attrib.get('name')};row={row.attrib.get('r')}",
                                )
                            )
            except (KeyError, ValueError, ET.ParseError, UnicodeDecodeError) as exc:
                raise ValueError("XLSX extraction failed") from exc
        output = "\n".join(x.text for x in fragments)
        if len(output) > policy.max_output_characters:
            raise ValueError("Extracted text exceeds configured maximum")
        return ExtractionResult(
            "", output, "ooxml-xlsx-extractor", "1", False, None, tuple(fragments)
        )
