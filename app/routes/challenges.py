from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.models import Challenge
from app.schema.schema import ChallengeCreate, ChallengeResponse
from app.services.ollama_service.ollama_service import generate_challenge
from datetime import datetime, timedelta
import time
from apscheduler.schedulers.background import BackgroundScheduler

router = APIRouter()
scheduler = BackgroundScheduler()

# Function to trigger nudges
def trigger_nudge():
    import requests  # Local import to avoid circular dependencies
    try:
        response = requests.get("http://localhost:8000/trigger-nudge")
        print("Nudge Triggered:", response.json())
    except Exception as e:
        print("Error triggering nudge:", e)

# Schedule nudge checks every 24 hours
scheduler.add_job(trigger_nudge, "interval", hours=24)
if not scheduler.running:
    scheduler.start()

@router.post("/", response_model=ChallengeResponse)
def create_challenge(data: ChallengeCreate, session: Session = Depends(get_session)):
    generated_text = generate_challenge(data)
    challenge = Challenge(**data.dict(), generated_challenge=generated_text)
    session.add(challenge)
    session.commit()
    session.refresh(challenge)
    return challenge

@router.get("/{challenge_id}", response_model=ChallengeResponse)
def get_challenge(challenge_id: int, session: Session = Depends(get_session)):
    challenge = session.exec(select(Challenge).where(Challenge.id == challenge_id)).first()
    if not challenge:
        return {"error": "Challenge not found"}
    return challenge

@router.post("/update-progress/{challenge_id}")
def update_progress(challenge_id: int, session: Session = Depends(get_session)):
    challenge = session.exec(select(Challenge).where(Challenge.id == challenge_id)).first()
    if not challenge:
        return {"error": "Challenge not found"}

    if challenge.status == "completed":
        return {"message": "Challenge already completed"}

    # Update progress
    challenge.progress += 1
    challenge.last_updated = datetime.utcnow()
    challenge.nudged = False  # Reset nudge flag since the user is active

    # Mark as completed if progress reaches duration
    if challenge.progress >= challenge.challenge_duration:
        challenge.status = "completed"

    session.add(challenge)
    session.commit()

    return {
        "message": "Progress updated",
        "progress": f"{challenge.progress}/{challenge.challenge_duration} days",
        "status": challenge.status
    }

def check_nudges(session: Session):
    nudge_threshold = datetime.utcnow() - timedelta(days=2)

    inactive_challenges = session.exec(
        select(Challenge).where(
            Challenge.last_updated < nudge_threshold,
            Challenge.status == "active",
            Challenge.nudged == False
        )
    ).all()

    nudged_users = []
    for challenge in inactive_challenges:
        challenge.nudged = True
        nudged_users.append(challenge.id)
        session.add(challenge)

    session.commit()
    return {"nudged_users": nudged_users}

@router.get("/trigger-nudge")
def trigger_nudge_endpoint(background_tasks: BackgroundTasks):
    """
    API endpoint that manually triggers a nudge.
    Runs in the background to avoid blocking the request.
    """
    background_tasks.add_task(check_nudges)
    return {"message": "Nudge check triggered"}

@router.get("/check-nudges", response_model=dict)
def check_nudges_endpoint(session: Session = Depends(get_session)):
    """
    API endpoint to manually check and process nudges.
    """
    result = check_nudges(session)
    return result

from app.db.database import get_session

def run_nudge_checker():
    from app.routes.challenges import check_nudges  # Avoid circular imports
    while True:
        time.sleep(300)  # Wait 5 minutes
        with next(get_session()) as session:
            check_nudges(session=session)
