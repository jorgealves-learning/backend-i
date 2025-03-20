FROM python:3.12-slim

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/
COPY . /app/

RUN poetry install --no-interaction

ENTRYPOINT [ "poetry", "run", "uvicorn" ]

CMD [ "fastapi_project.main:api", "--host", "0.0.0.0"]