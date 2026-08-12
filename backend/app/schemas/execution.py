from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExecutionCreate(BaseModel):
    task_id: int
    agent_id: int


class ExecutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    agent_id: int
    status: str
    result: str | None
    started_at: datetime
    completed_at: datetime | None
class ExecutionRunResponse(BaseModel):
    success: bool
    message: str
    execution_id: int
    task_id: int
    agent_id: int
    agent_name: str
    agent_role: str
    status: str
    result: str | None
    started_at: datetime
    completed_at: datetime | None

