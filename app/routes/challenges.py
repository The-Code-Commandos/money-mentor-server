from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.models import Challenge
from app.schema.schema import ChallengeCreate, ChallengeResponse
from app.services.ollama_service.ollama_service import generate_challenge
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from pydantic import BaseModel

router = APIRouter()
scheduler = BackgroundScheduler()

# Function to trigger nudges
def trigger_nudge():
    try:
        response = requests.get("http://localhost:8000/challenges/nudges/trigger")
        print("Nudge Triggered:", response.json())
    except Exception as e:
        print("Error triggering nudge:", e)

# Schedule nudge checks every 24 hours
scheduler.add_job(trigger_nudge, "interval", hours=24)
if not scheduler.running:
    scheduler.start()

@router.post("/", response_model=ChallengeResponse)
def create_challenge(data: ChallengeCreate, session: Session = Depends(get_session)):
    """
    Create a new financial challenge.
    """
    generated_text = generate_challenge(data)
    challenge = Challenge(**data.dict(), generated_challenge=generated_text)
    session.add(challenge)
    session.commit()
    session.refresh(challenge)
    return challenge

@router.get("/", response_model=list[ChallengeResponse])
def get_all_challenges(session: Session = Depends(get_session)):
    """
    Retrieve all challenges.
    """
    challenges = session.exec(select(Challenge)).all()
    return challenges

@router.get("/{challenge_id}", response_model=ChallengeResponse)
def get_challenge(challenge_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a specific challenge by ID.
    """
    challenge = session.exec(select(Challenge).where(Challenge.id == challenge_id)).first()
    if not challenge:
        return {"error": "Challenge not found"}
    return challenge

@router.post("/update-progress/{challenge_id}")
def update_progress(challenge_id: int, session: Session = Depends(get_session)):
    """
    Update the progress of an active challenge.
    """
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

class NudgeResponse(BaseModel):
    nudged_users: list[int]

@router.get("/nudges/check", response_model=NudgeResponse)
def check_nudges(session: Session = Depends(get_session)):
    """
    Check inactive users and nudge them.
    """
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
    return NudgeResponse(nudged_users=nudged_users)

@router.get("/nudges/trigger")
def trigger_nudge_endpoint(background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    API endpoint that manually triggers a nudge.
    Runs in the background to avoid blocking the request.
    """
    background_tasks.add_task(check_nudges, session)
    return {"message": "Nudge check triggered"}
