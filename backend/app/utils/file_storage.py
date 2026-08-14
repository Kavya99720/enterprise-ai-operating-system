from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parents[3]
DOCUMENT_STORAGE_DIR = BASE_DIR / "backend" / "storage" / "documents"


def save_document_file(
    filename: str,
    content: bytes,
) -> str:
    DOCUMENT_STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_name = Path(filename).name
    unique_filename = f"{uuid4().hex}_{safe_name}"

    file_path = DOCUMENT_STORAGE_DIR / unique_filename

    file_path.write_bytes(content)

    return str(
        file_path.relative_to(BASE_DIR)
    )