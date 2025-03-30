from sqlmodel import SQLModel, Field # type: ignore
from datetime import datetime

class Challenge(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    employment_type: str
    financial_goal: str  # Keep as string for flexibility
    investment_preference: str
    Monthly_income: float
    savings_rate: float
    spending_behavior: str
    debt_situation: str
    challenge_duration: int
    challenge_type: str
    commitment_level: str
    financial_fear: str
    generated_challenge: str
    progress: float = Field(default=0.0)  # Keep as float for accuracy
    status: str = Field(default="active")  # "active" or "completed"
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Add this field
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    nudged: bool = Field(default=False)
