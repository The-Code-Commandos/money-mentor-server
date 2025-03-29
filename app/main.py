from fastapi import FastAPI, BackgroundTasks # type: ignore
from app.routes.challenges import router as challenge_router
from app.routes.simulations import router as simulation_router
from app.routes.jargon import router as jargon_router
from app.db.database import create_db_and_tables
from app.routes.challenges import check_nudges
import time
import threading

app = FastAPI(title="Financial Confidence Coach API", version="1.0")

app.include_router(challenge_router, prefix="/challenges", tags=["Challenges"])
app.include_router(simulation_router, prefix="/simulations", tags=["Simulations"])
app.include_router(jargon_router, prefix="/jargon", tags=["Jargon-Free"])           

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    threading.Thread(target=run_nudge_checker, daemon=True).start()

def run_nudge_checker():
    while True:
        time.sleep(300)  # Wait 5 minutes
        check_nudges()
