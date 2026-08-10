from sqlalchemy.orm import Session

from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate):
    return task_repository.create_task(
        db=db,
        title=task_data.title,
        description=task_data.description,
    )


def get_task(db: Session, task_id: int):
    return task_repository.get_task(
        db=db,
        task_id=task_id,
    )


def get_tasks(db: Session):
    return task_repository.get_tasks(db=db)


def update_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
):
    task = task_repository.get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        return None

    return task_repository.update_task(
        db=db,
        task=task,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
    )


def delete_task(db: Session, task_id: int):
    task = task_repository.get_task(
        db=db,
        task_id=task_id,
    )

    if task is None:
        return False

    task_repository.delete_task(
        db=db,
        task=task,
    )

    return True