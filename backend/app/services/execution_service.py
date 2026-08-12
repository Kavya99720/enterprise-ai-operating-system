from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.repositories import agent_repository
from app.repositories import execution_repository
from app.repositories import task_repository


def execute_task(
    db: Session,
    task_id: int,
):
    task = task_repository.get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        return None

    if task.agent_id is None:
        return {
            "success": False,
            "message": "Task has no assigned agent.",
            "task_id": task.id,
        }

    agent = agent_repository.get_agent(
        db=db,
        agent_id=task.agent_id,
    )

    if agent is None:
        return {
            "success": False,
            "message": "Assigned agent not found.",
            "task_id": task.id,
            "agent_id": task.agent_id,
        }

    execution = execution_repository.create_execution(
        db=db,
        task_id=task.id,
        agent_id=agent.id,
    )

    execution = execution_repository.update_execution(
        db=db,
        execution=execution,
        status="completed",
        result="Task is ready for agent execution.",
        completed_at=datetime.now(timezone.utc),
    )

    return {
        "success": True,
        "message": "Task execution record created successfully.",
        "execution_id": execution.id,
        "task_id": task.id,
        "agent_id": agent.id,
        "agent_name": agent.name,
        "agent_role": agent.role,
        "status": execution.status,
        "result": execution.result,
        "started_at": execution.started_at,
        "completed_at": execution.completed_at,
    }


def get_execution(
    db: Session,
    execution_id: int,
):
    return execution_repository.get_execution(
        db=db,
        execution_id=execution_id,
    )


def get_executions(
    db: Session,
    task_id: int | None = None,
):
    return execution_repository.get_executions(
        db=db,
        task_id=task_id,
    )