from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.models import Challenge
from app.schema.schema import ChallengeCreate, ChallengeResponse
from app.services.ollama_service.ollama_service import generate_challenge
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import requests

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
        return {"message": "Challenge already completed", "progress": challenge.progress, "status": challenge.status}
    
    # Calculate progress increment based on financial goal and duration
    try:
        # Parse financial goal - remove currency symbol and convert to float
        financial_goal = float(challenge.financial_goal.replace("GH₵", "").strip()) if isinstance(challenge.financial_goal, str) else challenge.financial_goal
        
        # Guard against division by zero
        if challenge.challenge_duration <= 0:
            return {"error": "Invalid challenge duration"}
            
        increment = financial_goal / challenge.challenge_duration
    except (ValueError, AttributeError):
        # Default increment if financial_goal can't be parsed
        if challenge.challenge_duration <= 0:
            return {"error": "Invalid challenge duration"}
        increment = 100 / challenge.challenge_duration
    
    # Update progress - use float internally but store as integer in database
    new_progress = challenge.progress + increment
    challenge.progress = int(new_progress)  # Convert to int for storage
    challenge.last_updated = datetime.utcnow()
    challenge.nudged = False  # Reset nudge flag since the user is active
    
    # Mark as completed if progress reaches or exceeds goal
    if new_progress >= financial_goal:
        challenge.status = "completed"
        challenge.progress = int(financial_goal)  # Cap at goal, convert to int
    
    session.add(challenge)
    session.commit()
    
    return {
        "message": "Progress updated",
        "progress": challenge.progress,
        "status": challenge.status
    }

@router.get("/nudges/check", response_model=dict)
def check_nudges(session: Session = Depends(get_session)):
    """
    API endpoint to check inactive users and nudge them.
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
    return {"nudged_users": nudged_users}

@router.get("/nudges/trigger")
def trigger_nudge_endpoint(background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    """
    API endpoint that manually triggers a nudge.
    Runs in the background to avoid blocking the request.
    """
    background_tasks.add_task(check_nudges, session)
    return {"message": "Nudge check triggered"}
