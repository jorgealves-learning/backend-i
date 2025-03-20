from datetime import UTC, datetime
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from fastapi_project.main import api
from fastapi_project.models import Task

@pytest.fixture(scope="session")
def client():
    return TestClient(api)

@pytest.fixture()
def get_task(client)->Task:
    task = Task(title="Tasktitle", description="My details about the task", due_date=datetime.now(UTC))
    yield task 

def test_api_create_task(client, get_task):
    response = client.post("/task",data=get_task.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() is not None
    # here I delete the task to enforce creation of a new one on other tests
    client.delete(f"/task?title={get_task.title}")


def test_api_delete_task(client, get_task):
    # to test deletion i have to create it first :)
    response = client.post("/task",data=get_task.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() is not None

    response = client.delete(f"/task?title={get_task.title}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is None


def test_api_list_task(client, get_task):
    response = client.get("/task")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is not None