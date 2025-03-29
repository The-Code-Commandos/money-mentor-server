from fastapi import APIRouter, Depends # type: ignore
from sqlmodel import Session, select # type: ignore
from app.db.database import get_session
from app.models.models import Challenge
from app.schema.schema import ChallengeCreate, ChallengeResponse
from app.services.ollama_service.ollama_service import generate_challenge
from datetime import datetime, timedelta

router = APIRouter()

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

@router.get("/check-nudges")
def check_nudges(session: Session = Depends(get_session)):
    nudge_threshold = datetime.utcnow() - timedelta(days=2)  # Users inactive for 2+ days

    inactive_challenges = session.exec(
        select(Challenge).where(Challenge.last_updated < nudge_threshold, Challenge.status == "active", Challenge.nudged == False)
    ).all()

    nudged_users = []
    for challenge in inactive_challenges:
        challenge.nudged = True  # Mark nudge as sent
        nudged_users.append(challenge.id)
        session.add(challenge)

    session.commit()