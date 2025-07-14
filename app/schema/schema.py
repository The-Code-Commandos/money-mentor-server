from pydantic import BaseModel # type: ignore

class ChallengeCreate(BaseModel):
    employment_type: str
    financial_goal: str
    investment_preference: str
    monthly_income: float
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
