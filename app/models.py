from pydantic import BaseModel


class Event(BaseModel):
    id: int
    name: str
    description: str
    location: str
    date: str
    capacity: int
