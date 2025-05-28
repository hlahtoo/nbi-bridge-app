# app/api/endpoints/bridge.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.models import BridgeCore
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_bridges(limit: int = 10, db: Session = Depends(get_db)):
    bridges = db.query(BridgeCore).limit(limit).all()
    return [b.__dict__ for b in bridges]