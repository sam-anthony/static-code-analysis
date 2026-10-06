from pydantic import BaseModel


class Event(BaseModel):
    id: int
    name: str
    description: str
    location: str
    date: str
    capacity: int


class SignUpRequest(BaseModel):
    name: str
    email: str


class AttendeeResponse(BaseModel):
    id: int
    event_id: int
    name: str
    email: str
    on_waitlist: bool


class RosterEntry(BaseModel):
    event_id: int
    event_name: str
    attendee_name: str
    email: str
    on_waitlist: bool
