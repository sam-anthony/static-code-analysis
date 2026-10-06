from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from app.database import get_db
from app.models import Event

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=list[Event])
def list_events(db: Connection = Depends(get_db)):
    rows = db.execute("SELECT * FROM events ORDER BY date").fetchall()
    return [dict(row) for row in rows]


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: int, db: Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return dict(row)
