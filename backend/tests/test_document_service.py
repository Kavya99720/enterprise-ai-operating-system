from pathlib import Path

import pytest

from app.services.document_service import create_document_from_file


def test_create_document_from_txt(db_session):
    filename = "test.txt"
    content = b"Enterprise AI TXT extraction test."

    document = create_document_from_file(
        db_session,
        filename,
        content,
    )

    assert document.filename == filename
    assert document.file_type == ".txt"
    assert document.status == "processed"
    assert document.extracted_text == content.decode("utf-8")

    assert Path(document.storage_path).exists()


def test_create_document_rejects_unsupported_file(db_session):
    filename = "test.exe"
    content = b"unsupported content"

    with pytest.raises(ValueError, match="Unsupported document type"):
        create_document_from_file(
            db_session,
            filename,
            content,
        )