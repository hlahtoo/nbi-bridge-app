"""
Database setup and session management using SQLAlchemy.
"""
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine
from app.core.config import settings

# Load database URL from environment
DATABASE_URL = settings.DATABASE_URL

# Create the database engine with pre-ping for better connection health
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a session maker 
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for all ORM models
Base = declarative_base()

# Dependency to get a database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()