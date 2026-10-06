# Events API

A REST API for managing company-hosted events. The API provides access to event details including name, description, location, date, and capacity — serving as the back-end data layer for internal event management tooling and client-facing event discovery.

## Overview

Companies host a wide range of events — conferences, workshops, forums, and summits — across multiple locations. This API centralizes event data and exposes it through a consistent, lightweight interface that front-end applications and internal tools can consume.

## Tech Stack

- **Python 3** — application runtime
- **FastAPI** — web framework
- **SQLite** — embedded database
- **uvicorn** — ASGI server
- **pytest** — test suite

## Project Structure

```
/
├── app/
│   ├── database.py        # Database connection and initialization
│   ├── models.py          # Pydantic response models
│   └── routes/
│       └── events.py      # Event endpoints
├── tests/
│   └── test_events.py
├── main.py
└── requirements.txt
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive documentation is available at `http://localhost:8000/docs`. The SQLite database is created and seeded automatically on first run.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/events` | Returns all events, ordered by date |
| `GET` | `/events/{id}` | Returns a single event by ID |

### Example Response — `GET /events/1`

```json
{
  "id": 1,
  "name": "AI in the Enterprise",
  "description": "A full-day conference exploring how organizations are adopting AI responsibly at scale.",
  "location": "New York, NY",
  "date": "2026-09-18",
  "capacity": 300
}
```

## Running Tests

```bash
pytest
```
