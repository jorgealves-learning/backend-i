from datetime import datetime
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    # INFO: check https://github.com/fastapi/sqlmodel/discussions/1012#discussioncomment-10771004
    # to see how to make primary keys with 'autoincrement'
    title: str = Field(primary_key=True)
    description: str | None
    due_date: datetime
