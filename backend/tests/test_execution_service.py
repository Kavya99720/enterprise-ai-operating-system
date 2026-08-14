from types import SimpleNamespace
from unittest.mock import MagicMock

from app.services import execution_service


def test_execute_task_success(monkeypatch):
    db = MagicMock()

    task = SimpleNamespace(
        id=1,
        title="Analyze sales data",
        description="Find the top products.",
        status="pending",
        agent_id=None,
    )

    agent = SimpleNamespace(
        id=10,
        name="Data Analyst",
        role="Data Scientist",
        capabilities="Python, SQL",
    )

    execution = SimpleNamespace(
        id=100,
        task_id=1,
        agent_id=10,
        status="pending",
        result=None,
        started_at=None,
        completed_at=None,
    )

    monkeypatch.setattr(
        execution_service.task_repository,
        "get_task",
        lambda db, task_id: task,
    )

    monkeypatch.setattr(
        execution_service,
        "select_agent",
        lambda db, task: agent,
    )

    monkeypatch.setattr(
        execution_service.execution_repository,
        "create_execution",
        lambda db, task_id, agent_id: execution,
    )

    def update_execution(
        db,
        execution,
        status=None,
        result=None,
        completed_at=None,
    ):
        if status is not None:
            execution.status = status
        if result is not None:
            execution.result = result
        if completed_at is not None:
            execution.completed_at = completed_at
        return execution

    monkeypatch.setattr(
        execution_service.execution_repository,
        "update_execution",
        update_execution,
    )

    def update_task(db, task, status=None, agent_id=None):
        if status is not None:
            task.status = status
        if agent_id is not None:
            task.agent_id = agent_id
        return task

    monkeypatch.setattr(
        execution_service.task_repository,
        "update_task",
        update_task,
    )

    monkeypatch.setattr(
        execution_service,
        "run_agent",
        lambda agent, task: "Sales analysis completed.",
    )

    result = execution_service.execute_task(
        db=db,
        task_id=1,
    )

    assert result["success"] is True
    assert result["status"] == "completed"
    assert result["result"] == "Sales analysis completed."
    assert result["task_id"] == 1
    assert result["agent_id"] == 10
    assert result["agent_name"] == "Data Analyst"
    assert task.status == "completed"
    assert task.agent_id == 10
    assert execution.status == "completed"
    assert execution.result == "Sales analysis completed."
    assert execution.completed_at is not None


def test_execute_task_handles_agent_failure(monkeypatch):
    db = MagicMock()

    task = SimpleNamespace(
        id=2,
        title="Generate report",
        description="Create an AI report.",
        status="pending",
        agent_id=None,
    )

    agent = SimpleNamespace(
        id=20,
        name="Report Agent",
        role="AI Analyst",
        capabilities="Python, Reporting",
    )

    execution = SimpleNamespace(
        id=200,
        task_id=2,
        agent_id=20,
        status="pending",
        result=None,
        started_at=None,
        completed_at=None,
    )

    monkeypatch.setattr(
        execution_service.task_repository,
        "get_task",
        lambda db, task_id: task,
    )

    monkeypatch.setattr(
        execution_service,
        "select_agent",
        lambda db, task: agent,
    )

    monkeypatch.setattr(
        execution_service.execution_repository,
        "create_execution",
        lambda db, task_id, agent_id: execution,
    )

    def update_execution(
        db,
        execution,
        status=None,
        result=None,
        completed_at=None,
    ):
        if status is not None:
            execution.status = status
        if result is not None:
            execution.result = result
        if completed_at is not None:
            execution.completed_at = completed_at
        return execution

    monkeypatch.setattr(
        execution_service.execution_repository,
        "update_execution",
        update_execution,
    )

    def update_task(db, task, status=None, agent_id=None):
        if status is not None:
            task.status = status
        if agent_id is not None:
            task.agent_id = agent_id
        return task

    monkeypatch.setattr(
        execution_service.task_repository,
        "update_task",
        update_task,
    )

    def failing_run_agent(agent, task):
        raise RuntimeError("LLM provider request failed")

    monkeypatch.setattr(
        execution_service,
        "run_agent",
        failing_run_agent,
    )

    result = execution_service.execute_task(
        db=db,
        task_id=2,
    )

    assert result["success"] is False
    assert result["message"] == "Agent execution failed."
    assert result["status"] == "failed"
    assert result["result"] == "LLM provider request failed"
    assert result["task_id"] == 2
    assert result["agent_id"] == 20
    assert result["agent_name"] == "Report Agent"
    assert task.status == "failed"
    assert execution.status == "failed"
    assert execution.result == "LLM provider request failed"
    assert execution.completed_at is not None


def test_retry_execution_retries_failed_execution(monkeypatch):
    db = MagicMock()

    execution = SimpleNamespace(
        id=300,
        task_id=3,
        agent_id=30,
        status="failed",
        result="Previous LLM failure",
    )

    task = SimpleNamespace(
        id=3,
        title="Retry AI task",
        description="Retry the failed task.",
        status="failed",
        agent_id=30,
    )

    monkeypatch.setattr(
        execution_service.execution_repository,
        "get_execution",
        lambda db, execution_id: execution,
    )

    monkeypatch.setattr(
        execution_service.task_repository,
        "get_task",
        lambda db, task_id: task,
    )

    captured_status = {}

    def update_task(db, task, status=None, agent_id=None):
        if status is not None:
            task.status = status
            captured_status["status"] = status
        return task

    monkeypatch.setattr(
        execution_service.task_repository,
        "update_task",
        update_task,
    )

    retry_result = {
        "success": True,
        "message": "Task executed successfully.",
        "execution_id": 301,
        "task_id": 3,
        "status": "completed",
        "result": "Retry succeeded.",
    }

    monkeypatch.setattr(
        execution_service,
        "execute_task",
        lambda db, task_id: retry_result,
    )

    result = execution_service.retry_execution(
        db=db,
        execution_id=300,
    )

    assert captured_status["status"] == "pending"
    assert task.status == "pending"
    assert result == retry_result
