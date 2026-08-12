from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task


def create_task(
    db: Session,
    title: str,
    description: str | None = None,
    agent_id: int | None = None,
) -> Task:
    task = Task(
        title=title,
        description=description,
        agent_id=agent_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_task(
    db: Session,
    task_id: int,
) -> Task | None:
    statement = select(Task).where(Task.id == task_id)
    return db.scalar(statement)


def get_tasks(
    db: Session,
) -> list[Task]:
    statement = select(Task).order_by(Task.id.desc())
    return list(db.scalars(statement).all())


def update_task(
    db: Session,
    task: Task,
    title: str | None = None,
    description: str | None = None,
    status: str | None = None,
    agent_id: int | None = None,
) -> Task:
    if title is not None:
        task.title = title

    if description is not None:
        task.description = description

    if status is not None:
        task.status = status

    if agent_id is not None:
        task.agent_id = agent_id

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task,
) -> None:
    db.delete(task)
    db.commit()
