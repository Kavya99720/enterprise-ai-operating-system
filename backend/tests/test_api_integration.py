from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Enterprise AI Operating System is running"
    assert "environment" in data
def test_create_and_get_task(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Integration test task",
            "description": "Created through the FastAPI API",
        },
    )

    assert create_response.status_code == 201

    created = create_response.json()
    assert created["title"] == "Integration test task"
    assert created["description"] == "Created through the FastAPI API"
    assert created["status"] == "pending"
    assert created["id"] is not None

    task_id = created["id"]

    get_response = client.get(f"/api/v1/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id
def test_update_and_delete_task(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Task to update",
            "description": "Before update",
        },
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "Updated task",
            "description": "After update",
            "status": "completed",
        },
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "Updated task"
    assert updated["description"] == "After update"
    assert updated["status"] == "completed"

    delete_response = client.delete(f"/api/v1/tasks/{task_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/tasks/{task_id}")

    assert get_response.status_code == 404
def test_agent_crud(client):
    create_response = client.post(
        "/api/v1/agents",
        json={
            "name": "Integration Test Agent",
            "role": "tester",
            "description": "Agent created through API integration test",
            "capabilities": "testing,validation",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["name"] == "Integration Test Agent"
    assert created["role"] == "tester"
    assert created["capabilities"] == "testing,validation"
    assert created["status"] == "active"

    agent_id = created["id"]

    get_response = client.get(f"/api/v1/agents/{agent_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == agent_id

    update_response = client.put(
        f"/api/v1/agents/{agent_id}",
        json={
            "role": "integration-tester",
            "status": "inactive",
        },
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["role"] == "integration-tester"
    assert updated["status"] == "inactive"

    delete_response = client.delete(f"/api/v1/agents/{agent_id}")
    assert delete_response.status_code == 204

    final_response = client.get(f"/api/v1/agents/{agent_id}")
    assert final_response.status_code == 404
def test_execute_task_success(client, monkeypatch):
    from app.services import execution_service

    monkeypatch.setattr(
        execution_service,
        "run_agent",
        lambda agent, task: "Integration test execution result",
    )

    agent_response = client.post(
        "/api/v1/agents",
        json={
            "name": "Execution Test Agent API",
            "role": "executor",
            "description": "Agent for API integration testing",
            "capabilities": "testing,execution",
        },
    )

    assert agent_response.status_code == 201
    agent_id = agent_response.json()["id"]

    task_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Integration execution task",
            "description": "Execute through API",
            "agent_id": agent_id,
        },
    )

    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    execution_response = client.post(
        f"/api/v1/execution/tasks/{task_id}"
    )

    assert execution_response.status_code == 201

    execution = execution_response.json()
    assert execution["success"] is True
    assert execution["task_id"] == task_id
    assert execution["agent_id"] == agent_id
    assert execution["status"] == "completed"
    assert execution["result"] == "Integration test execution result"
    assert execution["execution_id"] is not None
def test_execution_retrieval_and_list(client, monkeypatch):
    from app.services import execution_service

    monkeypatch.setattr(
        execution_service,
        "run_agent",
        lambda agent, task: "Stored execution result",
    )

    agent_response = client.post(
        "/api/v1/agents",
        json={
            "name": "Execution Query Agent API",
            "role": "executor",
            "capabilities": "testing",
        },
    )
    assert agent_response.status_code == 201
    agent_id = agent_response.json()["id"]

    task_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Execution query task",
            "description": "Test execution retrieval",
            "agent_id": agent_id,
        },
    )
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]

    run_response = client.post(
        f"/api/v1/execution/tasks/{task_id}"
    )
    assert run_response.status_code == 201
    execution_id = run_response.json()["execution_id"]

    get_response = client.get(
        f"/api/v1/execution/{execution_id}"
    )
    assert get_response.status_code == 200
    assert get_response.json()["id"] == execution_id
    assert get_response.json()["status"] == "completed"
    assert get_response.json()["result"] == "Stored execution result"

    list_response = client.get(
        "/api/v1/execution",
        params={"task_id": task_id},
    )
    assert list_response.status_code == 200

    data = list_response.json()
    assert data["total"] == 1
    assert data["executions"][0]["id"] == execution_id
