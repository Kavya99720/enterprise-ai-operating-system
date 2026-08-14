from sqlalchemy.orm import Session

from app.repositories import document_repository
from app.schemas.document import DocumentCreate
from app.utils.document_extraction import extract_text_from_bytes
from app.utils.file_storage import save_document_file
from app.utils.file_validation import validate_document_filename


def create_document(
    db: Session,
    document_data: DocumentCreate,
):
    return document_repository.create_document(
        db,
        document_data,
    )


def create_document_from_file(
    db: Session,
    filename: str,
    content: bytes,
):
    file_type = validate_document_filename(filename)

    storage_path = save_document_file(
        filename,
        content,
    )

    document_data = DocumentCreate(
        filename=filename,
        file_type=file_type,
        storage_path=storage_path,
        extracted_text=None,
    )

    document = document_repository.create_document(
        db,
        document_data,
    )

    try:
        document_repository.update_document(
            db,
            document,
            status="processing",
        )

        extracted_text = extract_text_from_bytes(
            filename,
            content,
        )

        return document_repository.update_document(
            db,
            document,
            status="processed",
            extracted_text=extracted_text,
        )

    except Exception:
        document_repository.update_document(
            db,
            document,
            status="failed",
        )
        raise


def get_document(
    db: Session,
    document_id: int,
):
    return document_repository.get_document(
        db,
        document_id,
    )


def get_documents(
    db: Session,
):
    return document_repository.get_documents(db)