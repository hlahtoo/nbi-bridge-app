# app/main.py

from fastapi import FastAPI
from app.api.endpoints import bridge

app = FastAPI(title="Bridge API")

app.include_router(bridge.router, prefix="/bridges", tags=["Bridges"])