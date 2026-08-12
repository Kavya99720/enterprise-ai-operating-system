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

    best_agent = None
    best_score = 0

    for agent in agents:
        capabilities = (
            agent.capabilities.split(",")
            if agent.capabilities
            else []
        )

        score = 0

        for capability in capabilities:
            capability = capability.strip().lower()

            if capability and capability in task_text:
                score += 1

        if score > best_score:
            best_score = score
            best_agent = agent

    if best_agent is not None:
        return best_agent

    return agents[0]
