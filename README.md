
# Backend I

## Session 1 | Python Setup + First CLI
**Objective**
Set up the environment and run the first CLI command (`create-meeting`).

**Definition**
A reproducible environment with `uv` and a Typer-based CLI for the first system interactions.
Official references:
- uv docs: https://docs.astral.sh/uv/
- uv pip interface: https://docs.astral.sh/uv/pip/
- Typer docs: https://typer.tiangolo.com/

**Tutorial**
Commands:
```bash
mkdir meeting-note-assistant
cd meeting-note-assistant
git init
uv venv
source .venv/bin/activate
uv pip install typer
mkdir -p app
touch app/__init__.py
```
Code (`app/cli.py`):
```python
import typer

app = typer.Typer()

@app.command("hi")
def create_meeting(title: str, date: str, owner: str) -> None:
    typer.echo(f"Hello from Typer!!!")

if __name__ == "__main__":
    app()
```
Run:
```bash
python app/cli.py hi
```
Verification: command returns a meeting confirmation line.

**Exercise**
Create `create-meeting --title --date --owner` and print a summary in the terminal.

**Challenge**
Add simple date validation (`YYYY-MM-DD`) and a user-friendly error message.

## Session 2 | Data Modeling
**Objective**
Model `Meeting` and `ActionItem` in memory.

**Definition**
Modeling with `dataclasses` and collections to represent domain entities.
Official references:
- Dataclasses: https://docs.python.org/3/library/dataclasses.html
- Python typing: https://docs.python.org/3/library/typing.html

**Tutorial**
Commands:
```bash
mkdir -p app/domain app/services
touch app/domain/__init__.py
touch app/services/__init__.py
```
Code (`app/domain/models.py`):
```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class ActionItem:
    description: str
    owner: str
    due_date: str
    status: str = "open"

@dataclass
class Meeting:
    id: str
    title: str
    date: str
    owner: str
    participants: List[str] = field(default_factory=list)
    action_items: List[ActionItem] = field(default_factory=list)
```
Code (`app/services/memory_store.py`):
```python
from app.domain.models import Meeting

meetings: list[Meeting] = []
```
Verification: import both classes in REPL and instantiate sample objects.

**Exercise**
Implement `list-meetings` with readable output.

**Challenge**
Add a `Meeting -> ActionItem` relationship and task count per meeting.

## Session 3 | Functions and Modularization
**Objective**
Organize code into reusable modules.

**Definition**
Separation by responsibilities: `cli`, `domain`, `services`, `storage`.
Official references:
- Python modules: https://docs.python.org/3/tutorial/modules.html
- Python packages: https://packaging.python.org/en/latest/tutorials/packaging-projects/

**Tutorial**
Commands:
```bash
mkdir -p app/services
```
Code (`app/services/meeting_service.py`):
```python
from uuid import uuid4
from app.domain.models import Meeting
from app.services.memory_store import meetings


def create_meeting(title: str, date: str, owner: str) -> Meeting:
    meeting = Meeting(id=str(uuid4()), title=title, date=date, owner=owner)
    meetings.append(meeting)
    return meeting


def list_meetings() -> list[Meeting]:
    return meetings
```
Code update (`app/cli.py`):
```python
import typer
from app.services.meeting_service import create_meeting, list_meetings

app = typer.Typer()

@app.command("create-meeting")
def create_meeting_cmd(title: str, date: str, owner: str) -> None:
    meeting = create_meeting(title, date, owner)
    typer.echo(f"Created: {meeting.id}")

@app.command("list-meetings")
def list_meetings_cmd() -> None:
    for m in list_meetings():
        typer.echo(f"{m.id} | {m.date} | {m.title}")

if __name__ == "__main__":
    app()
```
Verification: both commands run without logic inside CLI handlers.

**Exercise**
Refactor `create-meeting` to call `create_meeting(...)` service.

**Challenge**
Add `show-meeting --id` without duplicating logic.

## Session 4 | JSON/CSV Persistence
**Objective**
Persist meetings locally in a reliable way.

**Definition**
Serialization/deserialization to preserve state between executions.
Official references:
- json: https://docs.python.org/3/library/json.html
- csv: https://docs.python.org/3/library/csv.html
- pathlib: https://docs.python.org/3/library/pathlib.html

**Tutorial**
Commands:
```bash
mkdir -p app/storage data
printf "[]" > data/meetings.json
```
Code (`app/storage/json_repository.py`):
```python
import json
from dataclasses import asdict
from pathlib import Path
from app.domain.models import Meeting, ActionItem

DB = Path("data/meetings.json")


def save_meetings(items: list[Meeting]) -> None:
    DB.parent.mkdir(parents=True, exist_ok=True)
    DB.write_text(json.dumps([asdict(m) for m in items], indent=2), encoding="utf-8")


def load_meetings() -> list[Meeting]:
    if not DB.exists():
        return []
    data = json.loads(DB.read_text(encoding="utf-8"))
    meetings: list[Meeting] = []
    for m in data:
        actions = [ActionItem(**a) for a in m.get("action_items", [])]
        meetings.append(Meeting(**{**m, "action_items": actions}))
    return meetings
```
Verification: create meetings, rerun command, and data remains in `data/meetings.json`.

**Exercise**
Persist and reload `Meeting` with participants.

**Challenge**
Export a CSV summary report with total action items per meeting.

## Session 5 | Validation and Exceptions
**Objective**
Apply business validations and error handling.

**Definition**
Predictable errors should become clear messages; invalid rules must be blocked.
Official references:
- Exceptions: https://docs.python.org/3/tutorial/errors.html
- datetime: https://docs.python.org/3/library/datetime.html

**Tutorial**
Commands:
```bash
mkdir -p app/core
printf "" > app/core/__init__.py
```
Code (`app/core/errors.py`):
```python
class ValidationError(Exception):
    pass

class NotFoundError(Exception):
    pass
```
Code (`app/core/validators.py`):
```python
from datetime import datetime
from app.core.errors import ValidationError


def validate_iso_date(value: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError("Date must be YYYY-MM-DD") from exc
```
Code update (`app/cli.py`):
```python
from app.core.errors import ValidationError

# inside command handler
try:
    # call service
    ...
except ValidationError as exc:
    typer.echo(f"Validation error: {exc}")
    raise typer.Exit(code=2)
```
Verification: invalid dates return clear errors and non-zero exit code.

**Exercise**
Block `ActionItem` creation without `owner` and without `due_date`.

**Challenge**
Create an exception-to-CLI error code mapping.

## Session 6 | Debugging and Logging
**Objective**
Debug bugs and improve observability.

**Definition**
Debugging and logging make diagnosis easier and reduce resolution time.
Official references:
- pdb: https://docs.python.org/3/library/pdb.html
- logging: https://docs.python.org/3/library/logging.html

**Tutorial**
Commands:
```bash
python -m pdb app/cli.py create-meeting --title "Bug" --date "2026-13-99" --owner "Jorge"
```
Code (`app/core/logging_config.py`):
```python
import logging


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
```
Code usage (`app/services/meeting_service.py`):
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Creating meeting", extra={"title": title, "date": date})
```
Verification: reproduce issue with debugger and confirm logs for create/list/error paths.

**Exercise**
Add `INFO` logs to create/list flow.

**Challenge**
Add `WARNING/ERROR` for invalid input and persistence failures.

## Session 7 | CLI Checkpoint
**Objective**
Consolidate CLI with basic CRUD and simple reporting.

**Definition**
Technical checkpoint validates fundamentals before API development.
Official references:
- argparse (CLI reference): https://docs.python.org/3/library/argparse.html
- Typer docs: https://typer.tiangolo.com/

**Tutorial**
Commands:
```bash
python app/cli.py create-meeting --title "Retro" --date "2026-03-04" --owner "Jorge"
python app/cli.py list-meetings
python app/cli.py show-meeting --id "<id>"
python app/cli.py delete-meeting --id "<id>"
```
Code (`app/services/report_service.py`):
```python
from app.domain.models import Meeting


def summary(meetings: list[Meeting]) -> dict:
    return {
        "meetings": len(meetings),
        "action_items": sum(len(m.action_items) for m in meetings),
    }
```
Verification: all CRUD commands and summary command work on persisted data.

**Exercise**
Deliver a working CLI with JSON persistence.

**Challenge**
Generate period report (`from_date`, `to_date`) with total meetings and tasks.

## Session 8 | HTTP/REST + FastAPI
**Objective**
Start FastAPI service and expose initial endpoints.

**Definition**
REST API for remote access to the meeting domain.
Official references:
- HTTP Semantics (IETF): https://httpwg.org/specs/rfc9110.html
- FastAPI docs: https://fastapi.tiangolo.com/
- Uvicorn docs: https://www.uvicorn.org/

**Tutorial**
Commands:
```bash
uv pip install fastapi uvicorn
mkdir -p app/api
printf "" > app/api/__init__.py
```
Code (`app/api/main.py`):
```python
from fastapi import FastAPI

app = FastAPI(title="Meeting Note Assistant API")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/meetings")
def list_meetings() -> list[dict]:
    return []
```
Run:
```bash
uvicorn app.api.main:app --reload
```
Verification: `/health` returns 200 and `/docs` renders.

**Exercise**
Create `GET /meetings/{meeting_id}` endpoint.

**Challenge**
Add correct status codes for missing resource (404).

## Session 9 | Pydantic and Contracts
**Objective**
Define robust input and output schemas.

**Definition**
Pydantic contracts protect API boundaries with structured validation.
Official references:
- Pydantic docs: https://docs.pydantic.dev/
- FastAPI request body: https://fastapi.tiangolo.com/tutorial/body/

**Tutorial**
Commands:
```bash
mkdir -p app/api
```
Code (`app/api/schemas.py`):
```python
from pydantic import BaseModel, Field

class MeetingCreate(BaseModel):
    title: str = Field(min_length=3)
    date: str
    owner: str = Field(min_length=2)

class MeetingRead(MeetingCreate):
    id: str
```
Code (`app/api/main.py` excerpt):
```python
from app.api.schemas import MeetingCreate, MeetingRead

@app.post("/meetings", response_model=MeetingRead, status_code=201)
def create_meeting(payload: MeetingCreate) -> MeetingRead:
    return MeetingRead(id="demo-id", **payload.model_dump())
```
Verification: invalid payload returns 422 with field details.

**Exercise**
Validate minimum `title` length and non-empty participants list.

**Challenge**
Add a standard error schema for 4xx responses.

## Session 10 | API Meetings CRUD
**Objective**
Build full meetings CRUD in API.

**Definition**
CRUD routes provide the operational backbone of the API.
Official references:
- FastAPI path operations: https://fastapi.tiangolo.com/tutorial/path-params/
- FastAPI status codes: https://fastapi.tiangolo.com/tutorial/response-status-code/

**Tutorial**
Commands:
```bash
mkdir -p app/api/routers
printf "" > app/api/routers/__init__.py
```
Code (`app/api/routers/meetings.py`):
```python
from fastapi import APIRouter, HTTPException, status
from app.api.schemas import MeetingCreate, MeetingRead

router = APIRouter(prefix="/meetings", tags=["meetings"])
DB: dict[str, dict] = {}

@router.post("", response_model=MeetingRead, status_code=status.HTTP_201_CREATED)
def create_meeting(payload: MeetingCreate):
    meeting_id = str(len(DB) + 1)
    DB[meeting_id] = {"id": meeting_id, **payload.model_dump()}
    return DB[meeting_id]

@router.get("/{meeting_id}", response_model=MeetingRead)
def get_meeting(meeting_id: str):
    item = DB.get(meeting_id)
    if not item:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return item
```
Verification: CRUD endpoints return expected status codes.

**Exercise**
Complete `PUT /meetings/{id}` with basic validation.

**Challenge**
Add `PATCH /meetings/{id}/status` with transition rules.

## Session 11 | Notes, Decisions, and Action Items
**Objective**
Add business objects associated with meetings.

**Definition**
Domain relationships increase the value of the Meeting Note Assistant.
Official references:
- FastAPI APIRouter: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- Pydantic nested models: https://docs.pydantic.dev/latest/concepts/models/

**Tutorial**
Commands:
```bash
# continue in existing API project
```
Code (`app/api/schemas.py` additions):
```python
class ActionItemCreate(BaseModel):
    description: str = Field(min_length=3)
    owner: str = Field(min_length=2)
    due_date: str

class ActionItemRead(ActionItemCreate):
    id: str
```
Code (`app/api/routers/action_items.py`):
```python
from fastapi import APIRouter, HTTPException
from app.api.schemas import ActionItemCreate

router = APIRouter(prefix="/meetings", tags=["action-items"])
ACTION_DB: dict[str, list[dict]] = {}

@router.post("/{meeting_id}/action-items")
def create_action_item(meeting_id: str, payload: ActionItemCreate):
    item = {"id": str(len(ACTION_DB.get(meeting_id, [])) + 1), **payload.model_dump()}
    ACTION_DB.setdefault(meeting_id, []).append(item)
    return item
```
Verification: you can create and list action items by meeting ID.

**Exercise**
Implement `POST /meetings/{id}/action-items`.

**Challenge**
Block completion of tasks without `owner` and valid due date.

## Session 12 | Filters, Sorting, and Pagination
**Objective**
Improve API query and usability.

**Definition**
Query params make search and navigation more efficient.
Official references:
- FastAPI query params: https://fastapi.tiangolo.com/tutorial/query-params/
- HTTP caching (concepts): https://httpwg.org/specs/rfc9111.html

**Tutorial**
Code (`app/api/routers/meetings.py` list endpoint):
```python
from fastapi import Query

@router.get("")
def list_meetings(
    owner: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items = list(DB.values())
    if owner:
        items = [m for m in items if m["owner"] == owner]
    items = sorted(items, key=lambda x: x["date"])
    return {"total": len(items), "items": items[offset : offset + limit]}
```
Run:
```bash
curl "http://127.0.0.1:8000/meetings?owner=Jorge&limit=10&offset=0"
```
Verification: response includes `total` and paginated items.

**Exercise**
Add `owner` filter for action items.

**Challenge**
Combine filters + pagination while keeping stable ordering.

## Session 13 | API Testing
**Objective**
Ensure quality with automated tests.

**Definition**
Tests validate success and error behavior before regressions.
Official references:
- pytest docs: https://docs.pytest.org/
- FastAPI testing: https://fastapi.tiangolo.com/tutorial/testing/

**Tutorial**
Commands:
```bash
uv pip install pytest httpx
mkdir -p tests
```
Code (`tests/test_meetings.py`):
```python
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_health_ok() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_meeting_ok() -> None:
    payload = {"title": "Planning", "date": "2026-03-10", "owner": "Jorge"}
    r = client.post("/meetings", json=payload)
    assert r.status_code == 201
```
Run:
```bash
pytest -q
```
Verification: tests pass and failures are reproducible.

**Exercise**
Write 3 tests for `POST /meetings` (success + 2 errors).

**Challenge**
Create reusable fixture for meetings and action items data.

## Session 14 | API Checkpoint
**Objective**
Consolidate API docs and error handling.

**Definition**
Checkpoint measures HTTP layer maturity before Django.
Official references:
- OpenAPI spec: https://spec.openapis.org/oas/latest.html
- FastAPI OpenAPI docs: https://fastapi.tiangolo.com/tutorial/metadata/

**Tutorial**
Commands:
```bash
pytest -q
curl http://127.0.0.1:8000/openapi.json | jq '.info'
```
Code (`app/api/main.py` metadata):
```python
app = FastAPI(
    title="Meeting Note Assistant API",
    version="0.2.0",
    description="Meetings, notes, and action items management",
)
```
Verification: docs are clear, errors are consistent, and regression tests pass.

**Exercise**
Publish API quality checklist and fix 2 gaps.

**Challenge**
Add aggregate endpoint `GET /dashboard/summary` with basic metrics.

## Session 15 | Django Setup + Models
**Objective**
Start Django for relational persistence and operations.

**Definition**
Django provides ORM and app structure for durable data.
Official references:
- Django start: https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Django models: https://docs.djangoproject.com/en/stable/topics/db/models/
- Django migrations: https://docs.djangoproject.com/en/stable/topics/migrations/

**Tutorial**
Commands:
```bash
uv pip install django
django-admin startproject backend_i_django
cd backend_i_django
python manage.py startapp meetings
```
Code (`backend_i_django/meetings/models.py`):
```python
from django.db import models

class Meeting(models.Model):
    title = models.CharField(max_length=150)
    date = models.DateField()
    owner = models.CharField(max_length=100)

class ActionItem(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="action_items")
    description = models.CharField(max_length=300)
    owner = models.CharField(max_length=100)
    due_date = models.DateField()
    status = models.CharField(max_length=20, default="open")
```
Run:
```bash
python manage.py makemigrations
python manage.py migrate
```
Verification: migration files created and DB tables available.

**Exercise**
Persist `Meeting` and list it in Django shell.

**Challenge**
Create `ForeignKey` relation and integrity rule for action items.

## Session 16 | Django Admin
**Objective**
Operate data productively through admin.

**Definition**
Admin speeds up operations, support, and manual validation.
Official references:
- Django admin site: https://docs.djangoproject.com/en/stable/ref/contrib/admin/

**Tutorial**
Commands:
```bash
python manage.py createsuperuser
```
Code (`backend_i_django/meetings/admin.py`):
```python
from django.contrib import admin
from .models import Meeting, ActionItem

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "owner")
    list_filter = ("date", "owner")
    search_fields = ("title", "owner")

@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "meeting", "owner", "due_date", "status")
    list_filter = ("status",)
```
Run:
```bash
python manage.py runserver
```
Verification: admin allows create/edit/list/search operations.

**Exercise**
Add `list_display` and `search_fields` for `Meeting`.

**Challenge**
Create custom admin action to mark tasks as completed.

## Session 17 | Authentication and Permissions
**Objective**
Apply basic access control.

**Definition**
Minimum security through users, groups, and permissions.
Official references:
- Django auth: https://docs.djangoproject.com/en/stable/topics/auth/
- Django permissions: https://docs.djangoproject.com/en/stable/topics/auth/default/

**Tutorial**
Commands:
```bash
python manage.py shell
```
Code (Django shell):
```python
from django.contrib.auth.models import Group, Permission
from meetings.models import Meeting

admin_group, _ = Group.objects.get_or_create(name="admin")
editor_group, _ = Group.objects.get_or_create(name="editor")
viewer_group, _ = Group.objects.get_or_create(name="viewer")

change_meeting = Permission.objects.get(codename="change_meeting")
view_meeting = Permission.objects.get(codename="view_meeting")

editor_group.permissions.add(change_meeting, view_meeting)
viewer_group.permissions.add(view_meeting)
```
Verification: users in `viewer` cannot edit, users in `editor` cannot delete.

**Exercise**
Configure `editor` group without meeting delete permission.

**Challenge**
Apply ownership-based permission rule for action items.

## Session 18 | AI I - Meeting Summaries
**Objective**
Integrate LLM for automatic note summaries.

**Definition**
Use model API to convert long notes into objective summaries.
Official references:
- OpenAI API docs: https://platform.openai.com/docs/api-reference
- OpenAI structured outputs guide: https://platform.openai.com/docs/guides/structured-outputs

**Tutorial**
Commands:
```bash
uv pip install openai
export OPENAI_API_KEY="<your_key>"
```
Code (`app/ai/summarizer.py`):
```python
from openai import OpenAI

client = OpenAI()


def summarize_meeting(notes: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize the meeting notes in max 5 bullet points:\n{notes}",
    )
    return response.output_text
```
Verification: same input returns concise summary suitable for meeting records.

**Exercise**
Generate short summary (max 5 bullets) for sample meeting.

**Challenge**
Add output format validation before persistence.

## Session 19 | AI II - Extraction and Classification
**Objective**
Extract action items and classify by priority/topic.

**Definition**
Structured AI output to feed task workflow.
Official references:
- OpenAI API docs: https://platform.openai.com/docs/api-reference
- JSON Schema: https://json-schema.org/

**Tutorial**
Code (`app/ai/extractor.py`):
```python
import json
from openai import OpenAI

client = OpenAI()


def extract_action_items(notes: str) -> list[dict]:
    prompt = (
        "Extract action items as JSON array with fields: "
        "description, owner, due_date, priority, topic.\n"
        f"Notes:\n{notes}"
    )
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    return json.loads(response.output_text)
```
Run:
```bash
python -c "from app.ai.extractor import extract_action_items; print(extract_action_items('Alice updates API by Friday'))"
```
Verification: output list can be mapped directly to `ActionItem` model.

**Exercise**
Extract 3 action items from meeting text.

**Challenge**
Add topic classification and reject incomplete items.

## Session 20 | AI Integration Robustness
**Objective**
Make AI integration robust, controlled, and predictable.

**Definition**
Resilience with timeout, retry, fallback, and cost control.
Official references:
- Tenacity (retry): https://tenacity.readthedocs.io/
- Python timeouts/concurrency: https://docs.python.org/3/library/asyncio-task.html

**Tutorial**
Commands:
```bash
uv pip install tenacity
```
Code (`app/ai/resilient_client.py`):
```python
from tenacity import retry, stop_after_attempt, wait_fixed
from openai import OpenAI

client = OpenAI()

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def summarize_with_retry(notes: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize in 5 bullets:\n{notes}",
        timeout=20,
    )
    return response.output_text


def summarize_with_fallback(notes: str) -> str:
    try:
        return summarize_with_retry(notes)
    except Exception:
        return "AI unavailable. Please write a manual summary."
```
Verification: simulate API failure and confirm deterministic fallback message.

**Exercise**
Implement fallback to manual extraction when AI fails.

**Challenge**
Add per-call cost metric and daily budget guard.

## Session 21 | Final Demo and Technical Defense
**Objective**
Demonstrate integrated project and justify technical decisions.

**Definition**
Close the CLI -> API -> Django -> AI loop with technical evidence.
Official references:
- FastAPI deployment: https://fastapi.tiangolo.com/deployment/
- Django deployment checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

**Tutorial**
Commands (demo script):
```bash
# 1) CLI flow
python app/cli.py create-meeting --title "Sprint" --date "2026-03-27" --owner "Jorge"
python app/cli.py list-meetings

# 2) API flow
uvicorn app.api.main:app --reload
curl -X POST http://127.0.0.1:8000/meetings -H 'content-type: application/json' -d '{"title":"Retro","date":"2026-03-27","owner":"Jorge"}'

# 3) Django flow
cd backend_i_django
python manage.py runserver

# 4) Test evidence
pytest -q
```
Code checklist (`DEMO_CHECKLIST.md`):
```md
- CLI create/list works
- API docs available at /docs
- CRUD returns expected status codes
- Django admin accessible and filtered
- AI summary works with fallback
- Tests green
```
Verification: 10-minute end-to-end demo runs without manual fixes.
