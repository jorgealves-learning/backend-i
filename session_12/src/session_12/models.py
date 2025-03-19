import os
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine

from session_12 import database


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    title: str
    description: str
    due_date: datetime
    is_done: bool = False


SQLModel.metadata.create_all(database.get_engine())