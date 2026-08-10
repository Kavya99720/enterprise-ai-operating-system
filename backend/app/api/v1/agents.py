from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from app.services import agent_service


router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post(
    "",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
):
    return agent_service.create_agent(
        db=db,
        agent_data=agent_data,
    )


@router.get(
    "",
    response_model=list[AgentResponse],
)
def get_agents(
    db: Session = Depends(get_db),
):
    return agent_service.get_agents(db=db)


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
)
def get_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    agent = agent_service.get_agent(
        db=db,
        agent_id=agent_id,
    )

    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )

    return agent


@router.put(
    "/{agent_id}",
    response_model=AgentResponse,
)
def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db),
):
    agent = agent_service.update_agent(
        db=db,
        agent_id=agent_id,
        agent_data=agent_data,
    )

    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )

    return agent


@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    deleted = agent_service.delete_agent(
        db=db,
        agent_id=agent_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found",
        )

    return None
