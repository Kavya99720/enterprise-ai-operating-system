from io import BytesIO
from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader


def extract_text_from_bytes(
    filename: str,
    content: bytes,
) -> str:
    extension = Path(filename).suffix.lower()

    if extension == ".txt":
        return content.decode("utf-8")

    if extension == ".pdf":
        return _extract_pdf_text(content)

    if extension == ".docx":
        return _extract_docx_text(content)

    raise ValueError(
        "Unsupported document type. Allowed types: TXT, PDF, DOCX."
    )


def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def _extract_docx_text(content: bytes) -> str:
    document = DocxDocument(BytesIO(content))

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)