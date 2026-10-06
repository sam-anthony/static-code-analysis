from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routes.events import router as events_router
from app.routes.attendees import router as attendees_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Events API", lifespan=lifespan)

app.include_router(events_router)
app.include_router(attendees_router)
