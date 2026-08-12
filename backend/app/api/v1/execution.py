from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import execution_service
from app.schemas.execution import ExecutionResponse, ExecutionRunResponse


router = APIRouter(
    prefix="/execution",
    tags=["Execution"],
)


@router.post(
    "/tasks/{task_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ExecutionRunResponse,
)
def execute_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    result = execution_service.execute_task(
        db=db,
        task_id=task_id,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if result.get("success") is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"],
        )

    return result


@router.get(
    "/{execution_id}",
    response_model=ExecutionResponse,
)
def get_execution(
    execution_id: int,
    db: Session = Depends(get_db),
):
    execution = execution_service.get_execution(
        db=db,
        execution_id=execution_id,
    )

    if execution is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found",
        )

    return execution


@router.get(
    "",
)
def get_executions(
    task_id: int | None = None,
    db: Session = Depends(get_db),
):
    return execution_service.get_executions(
        db=db,
        task_id=task_id,
    )


