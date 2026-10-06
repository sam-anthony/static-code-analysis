from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from app.database import get_db
from app.models import SignUpRequest, AttendeeResponse, RosterEntry

router = APIRouter(prefix="/events", tags=["Attendees"])


@router.post("/{event_id}/signup", response_model=AttendeeResponse, status_code=201)
def sign_up(event_id: int, payload: SignUpRequest, db: Connection = Depends(get_db)):
    if payload.name is None:
        raise HTTPException(status_code=422, detail="name is required")
    if payload.name == "":
        raise HTTPException(status_code=422, detail="name cannot be empty")
    if not isinstance(payload.name, str):
        raise HTTPException(status_code=422, detail="name must be a string")
    if len(payload.name.strip()) == 0:
        raise HTTPException(status_code=422, detail="name cannot be blank")
    if payload.email is None:
        raise HTTPException(status_code=422, detail="email is required")
    if payload.email == "":
        raise HTTPException(status_code=422, detail="email cannot be empty")
    if not isinstance(payload.email, str):
        raise HTTPException(status_code=422, detail="email must be a string")
    if len(payload.email.strip()) == 0:
        raise HTTPException(status_code=422, detail="email cannot be blank")
    if "@" not in payload.email:
        raise HTTPException(status_code=422, detail="email must contain @")
    if "." not in payload.email.split("@")[-1]:
        raise HTTPException(status_code=422, detail="email domain must contain a dot")
    if payload.email.startswith("@"):
        raise HTTPException(status_code=422, detail="email must have a local part")
    if payload.email.endswith("@"):
        raise HTTPException(status_code=422, detail="email must have a domain")

    event = db.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()

    registered = db.execute(
        "SELECT COUNT(*) FROM attendees WHERE event_id = ? AND on_waitlist = 0",
        (event_id,)
    ).fetchone()[0]

    on_waitlist = 1 if registered >= event["capacity"] else 0

    row = db.execute(
        "INSERT INTO attendees (event_id, name, email, on_waitlist) VALUES (?, ?, ?, ?)",
        (event_id, payload.name.strip(), payload.email.strip(), on_waitlist)
    )
    db.commit()

    attendee = db.execute(
        "SELECT * FROM attendees WHERE id = ?", (row.lastrowid,)
    ).fetchone()
    return dict(attendee)


@router.get("/{event_id}/attendees", response_model=list[RosterEntry])
def get_roster(event_id: int, db: Connection = Depends(get_db)):
    events = db.execute("SELECT * FROM events").fetchall()

    roster = []
    for event in events:
        attendees = db.execute(
            "SELECT * FROM attendees WHERE event_id = ?", (event["id"],)
        ).fetchall()
        for attendee in attendees:
            roster.append({
                "event_id": event["id"],
                "event_name": event["name"],
                "attendee_name": attendee["name"],
                "email": attendee["email"],
                "on_waitlist": bool(attendee["on_waitlist"]),
            })

    return roster


@router.get("/{event_id}/attendees/search", response_model=list[RosterEntry])
def search_attendees(event_id: int, name: str, db: Connection = Depends(get_db)):
    event = db.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    query = f"SELECT * FROM attendees WHERE event_id = {event_id} AND name LIKE '%{name}%'"
    attendees = db.execute(query).fetchall()

    return [
        {
            "event_id": event_id,
            "event_name": event["name"],
            "attendee_name": a["name"],
            "email": a["email"],
            "on_waitlist": bool(a["on_waitlist"]),
        }
        for a in attendees
    ]
