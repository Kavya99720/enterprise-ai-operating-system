from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.document import DocumentCreate


def create_document(
    db: Session,
    document_data: DocumentCreate,
) -> Document:
    document = Document(
        filename=document_data.filename,
        file_type=document_data.file_type,
        storage_path=document_data.storage_path,
        extracted_text=document_data.extracted_text,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def update_document(
    db: Session,
    document: Document,
    *,
    status: str | None = None,
    extracted_text: str | None = None,
) -> Document:
    if status is not None:
        document.status = status

    if extracted_text is not None:
        document.extracted_text = extracted_text

    db.commit()
    db.refresh(document)

    return document


def get_document(
    db: Session,
    document_id: int,
) -> Document | None:
    return db.query(Document).filter(
        Document.id == document_id
    ).first()


def get_documents(
    db: Session,
) -> list[Document]:
    return db.query(Document).order_by(
        Document.created_at.desc()
    ).all()