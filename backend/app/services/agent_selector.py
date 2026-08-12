from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.models.task import Task


def select_agent(
    db: Session,
    task: Task,
) -> Agent | None:
    if task.agent_id is not None:
        assigned_agent = db.scalar(
            select(Agent).where(
                Agent.id == task.agent_id,
                Agent.status == "active",
            )
        )

        if assigned_agent is not None:
            return assigned_agent

    task_text = f"{task.title} {task.description or ''}".lower()

    agents = list(
        db.scalars(
            select(Agent)
            .where(Agent.status == "active")
            .order_by(Agent.id.asc())
        ).all()
    )

    if not agents:
        return None

    for agent in agents:
        role_text = f"{agent.name} {agent.role} {agent.description or ''}".lower()

        if any(
            keyword in task_text
            for keyword in role_text.split()
            if len(keyword) >= 4
        ):
            return agent

    return agents[0]
