from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AgentCreate(BaseModel):
    name: str
    role: str
    description: str | None = None


class AgentUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    description: str | None = None
    status: str | None = None


class AgentResponse(BaseModel):
    id: int
    name: str
    role: str
    description: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
