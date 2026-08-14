from pathlib import Path


ALLOWED_DOCUMENT_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
}


def validate_document_filename(filename: str) -> str:
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValueError(
            "Unsupported document type. Allowed types: TXT, PDF, DOCX."
        )

    return extension