import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, "backend")

from main import app
from app.core.config import settings
from app.core.database import get_db
from app.models.agent import Agent
from app.models.document import Document
from app.models.execution import Execution
from app.models.task import Task


TEST_DATABASE_URL = settings.DATABASE_URL

test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def clean_test_data():
    db = TestSessionLocal()

    try:
        test_agents = db.query(Agent).filter(
            Agent.name.like("Execution %")
        ).all()

        test_agent_ids = [agent.id for agent in test_agents]

        if test_agent_ids:
            db.execute(
                delete(Execution).where(
                    Execution.agent_id.in_(test_agent_ids)
                )
            )

            db.execute(
                delete(Task).where(
                    Task.agent_id.in_(test_agent_ids)
                )
            )

            db.execute(
                delete(Agent).where(
                    Agent.id.in_(test_agent_ids)
                )
            )

            db.commit()

    finally:
        db.close()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.query(Document).delete()
        db.commit()
        db.close()