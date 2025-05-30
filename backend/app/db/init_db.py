"""
Initializes the database by dropping and recreating all tables using SQLAlchemy.
"""
from sqlalchemy import inspect
from app.db.session import engine
from app.db.base import Base 

def init_db():
    """
    Initializes the database by dropping and creating all tables based on models.py
    """
    # Drop all tables (if exist) and recreate from metadata
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 
  
    # Log created tables for verification
    inspector = inspect(engine)
    print("Tables created:", inspector.get_table_names())


if __name__ == "__main__":
    init_db()