"""
Defines the main API router and includes all bridge-related endpoints under the /bridges prefix.
from fastapi import APIRouter
"""
from fastapi import APIRouter
from app.api.endpoints import bridges

api_router = APIRouter()

# Include all routes from bridges.py under the /bridges path
api_router.include_router(bridges.router, prefix="/bridges", tags=["bridges"])