import pytest
import sqlite3
from fastapi.testclient import TestClient

from main import app
from app.database import get_db

DB_SCHEMA = """
    CREATE TABLE IF NOT EXISTS events (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        description TEXT    NOT NULL,
        location    TEXT    NOT NULL,
        date        TEXT    NOT NULL,
        capacity    INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS attendees (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id    INTEGER NOT NULL,
        name        TEXT    NOT NULL,
        email       TEXT    NOT NULL,
        on_waitlist INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (event_id) REFERENCES events(id)
    );
    INSERT INTO events (name, description, location, date, capacity) VALUES
        ('AI in the Enterprise', 'A full-day conference.', 'New York, NY', '2026-09-18', 300),
        ('DevOps & Platform Engineering Summit', 'Best practices in CI/CD.', 'Armonk, NY', '2026-10-02', 150),
        ('Cloud Architecture Workshop', 'Hands-on workshop.', 'Austin, TX', '2026-11-13', 60),
        ('Security & Compliance Forum', 'Panel discussions.', 'Research Triangle Park, NC', '2026-12-04', 200);
"""


@pytest.fixture
def client(tmp_path):
    db_path = str(tmp_path / "test.db")

    setup = sqlite3.connect(db_path)
    setup.executescript(DB_SCHEMA)
    setup.commit()
    setup.close()

    def override_get_db():
        db = sqlite3.connect(db_path, check_same_thread=False)
        db.row_factory = sqlite3.Row
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_list_events(client):
    response = client.get("/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4


def test_get_event(client):
    response = client.get("/events/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "location" in data
    assert "date" in data
    assert "capacity" in data


def test_get_event_not_found(client):
    response = client.get("/events/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_events_ordered_by_date(client):
    response = client.get("/events")
    data = response.json()
    dates = [e["date"] for e in data]
    assert dates == sorted(dates)


def test_signup(client):
    response = client.post("/events/1/signup", json={"name": "Jane Smith", "email": "jane@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["event_id"] == 1
    assert data["name"] == "Jane Smith"
    assert data["email"] == "jane@example.com"
    assert data["on_waitlist"] == False


def test_signup_waitlist(client):
    response = client.post("/events/3/signup", json={"name": "Jane Smith", "email": "jane@example.com"})
    assert response.status_code == 201

    response2 = client.post("/events/3/signup", json={"name": "Bob Jones", "email": "bob@example.com"})
    assert response2.status_code == 201


def test_get_roster(client):
    client.post("/events/1/signup", json={"name": "Jane Smith", "email": "jane@example.com"})
    response = client.get("/events/1/attendees")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(a["attendee_name"] == "Jane Smith" for a in data)


def test_search_attendees(client):
    client.post("/events/1/signup", json={"name": "Jane Smith", "email": "jane@example.com"})
    response = client.get("/events/1/attendees/search?name=Jane")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["attendee_name"] == "Jane Smith"
