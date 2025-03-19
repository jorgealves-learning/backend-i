FROM python:3.12-slim

WORKDIR /workspace

RUN pip install poetry

COPY . .

RUN poetry install --quiet --no-interaction

ENTRYPOINT [ "poetry", "run", "uvicorn" ]

CMD [ "session_12.main:api", "--host", "0.0.0.0"]