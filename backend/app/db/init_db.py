# app/db/init_db.py
from sqlalchemy import inspect
from app.db.session import engine
from app.db.base import Base  # Base must import all models to work

def init_db():
    print("database initialized")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine) 
    inspector = inspect(engine)
    print("Tables created:", inspector.get_table_names())

# 👇 This line is essential
if __name__ == "__main__":
    init_db()