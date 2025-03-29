from sqlmodel import SQLModel, Field # type: ignore
from datetime import datetime

class Challenge(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
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
    generated_challenge: str
    progress: int = Field(default=0)  
    status: str = Field(default="active")  # "active" or "completed"
    last_updated: datetime = Field(default_factory=datetime.utcnow)  # Track last progress update
    nudged: bool = Field(default=False)  # Track if a nudge has been sent
