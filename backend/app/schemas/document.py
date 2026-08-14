from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentCreate(BaseModel):
    filename: str
    file_type: str
    storage_path: str
    extracted_text: str | None = None


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    storage_path: str
    status: str
    extracted_text: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
