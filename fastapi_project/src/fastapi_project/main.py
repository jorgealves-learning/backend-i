from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi_project import database
from fastapi_project.models import Task
from fastapi import FastAPI, Form, status
from fastapi.exceptions import HTTPException

api = FastAPI(
    title="TODO Etic_Algarve API"
)

@api.get("/task",status_code=status.HTTP_200_OK)
def list_task():
    return database.get_all_tasks()

@api.post("/task")
def create_task(data: Annotated[Task,Form()]):
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    database.create_task(task=data)
    return JSONResponse({"status": "created"}, status_code=status.HTTP_201_CREATED)

@api.delete("/task", status_code=status.HTTP_200_OK)
def delete_task(title: str):
    assert title 
    database.delete_task(title=title)