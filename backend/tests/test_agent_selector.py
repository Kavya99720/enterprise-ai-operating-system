from types import SimpleNamespace
from unittest.mock import MagicMock

from app.services.agent_selector import select_agent


def test_select_agent_prefers_assigned_active_agent():
    db = MagicMock()

    task = SimpleNamespace(
        id=1,
        title="Analyze sales data",
        description="Use Python and SQL.",
        agent_id=10,
    )

    assigned_agent = SimpleNamespace(
        id=10,
        name="Data Analyst",
        role="Data Scientist",
        capabilities="Python, SQL",
        status="active",
    )

    db.scalar.return_value = assigned_agent

    result = select_agent(
        db=db,
        task=task,
    )

    assert result is assigned_agent
    assert result.id == 10
    assert result.status == "active"

def test_select_agent_matches_capabilities(monkeypatch):
    db = MagicMock()

    task = SimpleNamespace(
        id=2,
        title="Build a machine learning model",
        description="Use Python and scikit-learn.",
        agent_id=None,
    )

    data_agent = SimpleNamespace(
        id=20,
        name="Data Scientist",
        role="ML Engineer",
        capabilities="Python, Machine Learning, scikit-learn",
        status="active",
    )

    report_agent = SimpleNamespace(
        id=30,
        name="Report Agent",
        role="Business Analyst",
        capabilities="Reporting, Documentation",
        status="active",
    )

    db.scalar.return_value = None
    db.scalars.return_value.all.return_value = [
        data_agent,
        report_agent,
    ]

    result = select_agent(
        db=db,
        task=task,
    )

    assert result is data_agent
    assert result.id == 20
    assert result.name == "Data Scientist"

def test_select_agent_ignores_inactive_assigned_agent(monkeypatch):
    db = MagicMock()

    task = SimpleNamespace(
        id=3,
        title="Generate business report",
        description="Create documentation.",
        agent_id=40,
    )

    inactive_agent = SimpleNamespace(
        id=40,
        name="Inactive Analyst",
        role="Analyst",
        capabilities="Reporting",
        status="inactive",
    )

    active_agent = SimpleNamespace(
        id=50,
        name="Active Report Agent",
        role="Business Analyst",
        capabilities="Reporting, Documentation",
        status="active",
    )

    db.scalar.return_value = None
    db.scalars.return_value.all.return_value = [
        active_agent,
    ]

    result = select_agent(
        db=db,
        task=task,
    )

    assert result is active_agent
    assert result.id == 50
    assert result.status == "active"

def test_select_agent_falls_back_to_first_active_agent():
    db = MagicMock()

    task = SimpleNamespace(
        id=4,
        title="Prepare presentation",
        description="Create slides for the quarterly meeting.",
        agent_id=None,
    )

    first_agent = SimpleNamespace(
        id=60,
        name="General Agent",
        role="General Assistant",
        capabilities="Python, SQL",
        status="active",
    )

    second_agent = SimpleNamespace(
        id=70,
        name="ML Agent",
        role="Machine Learning Engineer",
        capabilities="Machine Learning, TensorFlow",
        status="active",
    )

    db.scalar.return_value = None
    db.scalars.return_value.all.return_value = [
        first_agent,
        second_agent,
    ]

    result = select_agent(
        db=db,
        task=task,
    )

    assert result is first_agent
    assert result.id == 60
    assert result.status == "active"
