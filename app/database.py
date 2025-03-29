from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Float, DateTime # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker, relationship # type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

# SQLite-specific configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./financial_coach.db")

# Enable SQLite WAL mode for better concurrency
connect_args = {
    "check_same_thread": False,
    "timeout": 30,  # Set timeout to 30 seconds
    "isolation_level": "IMMEDIATE"  # Better for concurrent access
}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_size=5,  # Smaller pool size for SQLite
    max_overflow=2,
    echo=False  # Set to True for debugging SQL queries
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # Added length constraint
    hashed_password = Column(String(128))  # For hashed passwords
    email = Column(String(100), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    
    # Financial profile
    income_range = Column(String(20))  # e.g., "0-1000", "1000-3000"
    primary_goal = Column(String(50))  # e.g., "saving", "investing"
    risk_tolerance = Column(Integer)  # 1-5 scale
    
    challenges = relationship("UserChallenge", back_populates="user")
    progress = relationship("UserProgress", back_populates="user")

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(500))
    difficulty = Column(Integer)  # 1-5 scale
    category = Column(String(30))  # e.g., "saving", "investing", "learning"
    reward_points = Column(Integer)
    
    user_challenges = relationship("UserChallenge", back_populates="challenge")

class UserChallenge(Base):
    __tablename__ = "user_challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="challenges")
    challenge = relationship("Challenge", back_populates="user_challenges")

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    confidence_score = Column(Float)  # 0-100 scale
    total_points = Column(Integer)
    current_streak = Column(Integer)  # days of consecutive activity
    last_active_date = Column(DateTime)  # Track last activity for streaks
    
    user = relationship("User", back_populates="progress")

# Database utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database, create tables and insert initial data"""
    Base.metadata.create_all(bind=engine)
    
    # Optionally add some initial challenges
    db = SessionLocal()
    try:
        if not db.query(Challenge).first():
            initial_challenges = [
                Challenge(
                    title="Save your first GHS 5",
                    description="Skip one small expense today and save GHS 5 in your DigiSave account",
                    difficulty=1,
                    category="saving",
                    reward_points=10
                ),
                Challenge(
                    title="Learn about Eurobonds",
                    description="Read a simple explanation about what Eurobonds are",
                    difficulty=2,
                    category="learning",
                    reward_points=15
                ),
                # Add more initial challenges as needed
            ]
            db.add_all(initial_challenges)
            db.commit()
    finally:
        db.close()

# Initialize the database when this module is imported
init_db()