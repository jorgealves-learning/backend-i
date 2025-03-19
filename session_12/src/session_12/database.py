import os
from sqlalchemy import Engine
from sqlmodel import Session, create_engine
from session_12.models import Task

def get_engine()->Engine:
    DB_USER = os.getenv("DB_USER", None)
    DB_PASS = os.getenv("DB_PASS", None)
    DB_HOST = os.getenv("DB_HOST", None)
    DB_PORT = os.getenv("DB_PORT", None)
    DB_NAME = os.getenv("DB_NAME", None)
    return create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def get_session()->Session:
    return Session(get_engine())

def create_task(task: Task):
    assert task
    with get_session() as session:
        session.add(task)
        session.commit()
        