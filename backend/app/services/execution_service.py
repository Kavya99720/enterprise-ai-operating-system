from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.agents.agent_runner import run_agent
from app.repositories import execution_repository
from app.repositories import task_repository
from app.services.agent_selector import select_agent


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

    if task.status == "running":
        return {
            "success": False,
            "message": "Task is already running.",
            "task_id": task.id,
            "status": "running",
        }

    if task.status == "completed":
        return {
            "success": False,
            "message": "Task has already been completed.",
            "task_id": task.id,
            "status": "completed",
        }

    agent = select_agent(
        db=db,
        task=task,
    )

    if agent is None:
        return {
            "success": False,
            "message": "No active agent available for this task.",
            "task_id": task.id,
        }

    if task.agent_id != agent.id:
        task = task_repository.update_task(
            db=db,
            task=task,
            agent_id=agent.id,
        )

    task = task_repository.update_task(
        db=db,
        task=task,
        status="running",
    )

    execution = execution_repository.create_execution(
        db=db,
        task_id=task.id,
        agent_id=agent.id,
    )

    execution = execution_repository.update_execution(
        db=db,
        execution=execution,
        status="running",
    )

    try:
        result = run_agent(
            agent=agent,
            task=task,
        )

        completed_at = datetime.now(timezone.utc)

        execution = execution_repository.update_execution(
            db=db,
            execution=execution,
            status="completed",
            result=result,
            completed_at=completed_at,
        )

        task_repository.update_task(
            db=db,
            task=task,
            status="completed",
        )

        return {
            "success": True,
            "message": "Task executed successfully.",
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

    except Exception as exc:
        completed_at = datetime.now(timezone.utc)

        execution = execution_repository.update_execution(
            db=db,
            execution=execution,
            status="failed",
            result=str(exc),
            completed_at=completed_at,
        )

        task_repository.update_task(
            db=db,
            task=task,
            status="failed",
        )

        return {
            "success": False,
            "message": "Agent execution failed.",
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


def retry_execution(
    db: Session,
    execution_id: int,
):
    execution = execution_repository.get_execution(
        db=db,
        execution_id=execution_id,
    )

    if execution is None:
        return None

    if execution.status != "failed":
        return {
            "success": False,
            "message": "Only failed executions can be retried.",
            "execution_id": execution.id,
            "status": execution.status,
        }

    task = task_repository.get_task(
        db=db,
        task_id=execution.task_id,
    )

    if task is None:
        return {
            "success": False,
            "message": "Task associated with execution was not found.",
            "execution_id": execution.id,
        }

    task_repository.update_task(
        db=db,
        task=task,
        status="pending",
    )

    return execute_task(
        db=db,
        task_id=execution.task_id,
    )


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
    status: str | None = None,
):
    executions = execution_repository.get_executions(
        db=db,
        task_id=task_id,
        status=status,
    )

    return {
        "total": len(executions),
        "executions": executions,
    }
