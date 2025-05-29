from fastapi import APIRouter
from app.api.endpoints import bridges

api_router = APIRouter()
api_router.include_router(bridges.router, prefix="/bridges", tags=["bridges"])