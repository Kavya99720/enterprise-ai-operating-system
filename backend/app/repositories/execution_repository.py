from datetime import datetime

from sqlalchemy.orm import Session

from app.models.execution import Execution


def create_execution(
    db: Session,
    task_id: int,
    agent_id: int,
) -> Execution:
    execution = Execution(
        task_id=task_id,
        agent_id=agent_id,
        status="pending",
    )

    db.add(execution)
    db.commit()
    db.refresh(execution)

    return execution


def get_execution(
    db: Session,
    execution_id: int,
) -> Execution | None:
    return (
        db.query(Execution)
        .filter(Execution.id == execution_id)
        .first()
    )


def get_executions(
    db: Session,
    task_id: int | None = None,
) -> list[Execution]:
    query = db.query(Execution)

    if task_id is not None:
        query = query.filter(Execution.task_id == task_id)

    return query.order_by(Execution.id.desc()).all()


def update_execution(
    db: Session,
    execution: Execution,
    status: str | None = None,
    result: str | None = None,
    completed_at: datetime | None = None,
) -> Execution:
    if status is not None:
        execution.status = status

    if result is not None:
        execution.result = result

    if completed_at is not None:
        execution.completed_at = completed_at

    db.commit()
    db.refresh(execution)

    return execution