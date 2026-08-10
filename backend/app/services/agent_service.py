from sqlalchemy.orm import Session

from app.repositories import agent_repository
from app.schemas.agent import AgentCreate, AgentUpdate


def create_agent(db: Session, agent_data: AgentCreate):
    return agent_repository.create_agent(
        db=db,
        name=agent_data.name,
        role=agent_data.role,
        description=agent_data.description,
    )


def get_agent(db: Session, agent_id: int):
    return agent_repository.get_agent(
        db=db,
        agent_id=agent_id,
    )


def get_agents(db: Session):
    return agent_repository.get_agents(db=db)


def update_agent(
    db: Session,
    agent_id: int,
    agent_data: AgentUpdate,
):
    agent = agent_repository.get_agent(
        db=db,
        agent_id=agent_id,
    )

    if agent is None:
        return None

    return agent_repository.update_agent(
        db=db,
        agent=agent,
        name=agent_data.name,
        role=agent_data.role,
        description=agent_data.description,
        status=agent_data.status,
    )


def delete_agent(db: Session, agent_id: int):
    agent = agent_repository.get_agent(
        db=db,
        agent_id=agent_id,
    )

    if agent is None:
        return False

    agent_repository.delete_agent(
        db=db,
        agent=agent,
    )

    return True
