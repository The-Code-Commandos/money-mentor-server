from fastapi import FastAPI, BackgroundTasks # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from app.routes.challenges import router as challenge_router
from app.routes.simulations import router as simulation_router
from app.routes.jargon import router as jargon_router
from app.db.database import create_db_and_tables
from app.routes.challenges import check_nudges
import time
import threading
from app.db.database import get_session
from sqlmodel import Session

app = FastAPI(title="Financial Confidence Coach API", version="1.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

app.include_router(challenge_router, prefix="/challenges", tags=["Challenges"])
app.include_router(simulation_router, prefix="/simulations", tags=["Simulations"])
app.include_router(jargon_router, prefix="/jargon", tags=["Jargon-Free"])           

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    threading.Thread(target=run_nudge_checker, daemon=True).start()

def run_nudge_checker():
    from app.routes.challenges import check_nudges  # Import here to avoid circular imports
    while True:
        time.sleep(300)  # Wait 5 minutes
        with next(get_session()) as session:  # Manually create a session
            check_nudges(session=session)
