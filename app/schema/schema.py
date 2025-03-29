from pydantic import BaseModel

class ChallengeCreate(BaseModel):
    employment_type: str
    financial_goal: str
    investment_preference: str
    savings_rate: float
    spending_behavior: str
    debt_situation: str
    challenge_duration: int
    challenge_type: str
    commitment_level: str
    financial_fear: str

class ChallengeResponse(BaseModel):
    id: int
    generated_challenge: str
    challenge_duration: int
    challenge_type: str
    status: str
