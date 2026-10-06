# Events API

A REST API for managing company-hosted events. The API provides access to event details including name, description, location, date, and capacity — serving as the back-end data layer for internal event management tooling and client-facing event discovery.

## Overview

Companies host a wide range of events — conferences, workshops, forums, and summits — across multiple locations. This API centralizes event data and exposes it through a consistent, lightweight interface that front-end applications and internal tools can consume.

Attendees can register for events through the API. If an event is at capacity, registrants are automatically added to a waitlist. Event organizers can view the full roster and search for specific attendees by name.

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
│   ├── models.py          # Pydantic request and response models
│   └── routes/
│       ├── events.py      # Event endpoints
│       └── attendees.py   # Attendee endpoints
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

### Events

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/events` | Returns all events, ordered by date |
| `GET` | `/events/{id}` | Returns a single event by ID |

### Attendees

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/events/{id}/signup` | Register an attendee for an event |
| `GET` | `/events/{id}/attendees` | Returns the full roster for an event |
| `GET` | `/events/{id}/attendees/search` | Search the roster by attendee name |

### Example — `GET /events/1`

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

### Example — `POST /events/1/signup`

Request:
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com"
}
```

Response:
```json
{
  "id": 1,
  "event_id": 1,
  "name": "Jane Smith",
  "email": "jane@example.com",
  "on_waitlist": false
}
```

## Running Tests

```bash
pytest
```
