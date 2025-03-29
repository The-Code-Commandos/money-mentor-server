from sqlmodel import SQLModel, Session, create_engine # type: ignore

DATABASE_URL = "sqlite:///./financial_coach.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)