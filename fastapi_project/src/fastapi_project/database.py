import os
from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, create_engine, select
from fastapi_project.models import Task

def get_engine()->Engine:
    DB_USER = os.getenv("DB_USER", None)
    DB_PASS = os.getenv("DB_PASS", None)
    DB_HOST = os.getenv("DB_HOST", None)
    DB_PORT = os.getenv("DB_PORT", None)
    DB_NAME = os.getenv("DB_NAME", None)
    return create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)

def get_session()->Session:
    return Session(get_engine())

def create_task(task: Task):
    assert task
    with get_session() as session:
        session.add(task)
        session.commit()

def update_task(title: str, task: Task):
    assert title
    assert task
    with get_session() as session:
        statement = select(Task).where(Task.title == title)
        query = session.exec(statement=statement)
        updated_task = query.one()
        updated_task.description = task.description
        updated_task.due_date = task.due_date
        session.add(update_task)
        session.commit()
        
def delete_task(title: str):
    assert title
    with get_session() as session:
        # creation of the SQL statement
        statement = select(Task).where(Task.title == title)
        # query execution
        query = session.exec(statement=statement)
        # Take the first result
        task = query.one()
        assert task
        session.delete(task)
        session.commit()


def get_all_tasks()-> list[Task]:
    results: list[Task] = []
    with get_session() as session:
        #query to get all tasks from the table
        results = session.exec(select(Task)).all()
    return results


SQLModel.metadata.create_all(get_engine())