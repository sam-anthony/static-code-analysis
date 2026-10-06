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
