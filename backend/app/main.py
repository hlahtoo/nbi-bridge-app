"""
Main entry point for FastAPI app with CORS and API routing setup.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router

app = FastAPI()

# Enable CORS for frontend (e.g., React app on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    #  Modify for production based on where the frontend is hosted
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes under the /api prefix
app.include_router(api_router, prefix="/api")