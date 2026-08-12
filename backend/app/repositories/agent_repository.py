from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent import Agent


def create_agent(
    db: Session,
    name: str,
    role: str,
    description: str | None = None,
    capabilities: str | None = None,
) -> Agent:
    agent = Agent(
        name=name,
        role=role,
        description=description,
        capabilities=capabilities,
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return agent


def get_agent(
    db: Session,
    agent_id: int,
) -> Agent | None:
    statement = select(Agent).where(Agent.id == agent_id)
    return db.scalar(statement)


def get_agents(
    db: Session,
) -> list[Agent]:
    statement = select(Agent).order_by(Agent.id.desc())
    return list(db.scalars(statement).all())


def update_agent(
    db: Session,
    agent: Agent,
    name: str | None = None,
    role: str | None = None,
    description: str | None = None,
    capabilities: str | None = None,
    status: str | None = None,
) -> Agent:
    if name is not None:
        agent.name = name

    if role is not None:
        agent.role = role

    if description is not None:
        agent.description = description

    if capabilities is not None:
        agent.capabilities = capabilities

    if status is not None:
        agent.status = status

    db.commit()
    db.refresh(agent)

    return agent


def delete_agent(
    db: Session,
    agent: Agent,
) -> None:
    db.delete(agent)
    db.commit()
