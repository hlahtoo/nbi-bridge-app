"""
Bridge API Router

This module defines the FastAPI endpoints for querying bridge data from the database.
It supports both basic bridge info and detailed bridge attributes via spatial queries.

Endpoints:
-----------
1. GET `/api/bridges/`
    - Returns a list of bridge core records (basic info).
    - Query Param: `limit` (int): Max number of records to return (default=100).

2. POST `/api/bridges/batch`
    - Accepts a list of map tile coordinates and returns bridges intersecting them.
    - Supports two modes:
        • `single`: One bridge per tile (best rated, worst condition, etc.)
        • `batch`: All bridges intersecting union of tiles
    - Query Params:
        • `zoom` (int): Tile zoom level
        • `filterKey` (str): One of ["lowestRating", "highestADT", "worstBridgeCondition"]
        • `limit` (int): Max records to return

3. GET `/api/bridges/detail/{structure_number}`
    - Fetches detailed info for a specific bridge by its structure number.

Raises:
--------
- 400 Bad Request: If query parameters or tile input are invalid
- 404 Not Found: If a specific bridge structure number doesn't exist
- 500 Internal Server Error: For unhandled database or server issues
"""
from fastapi import APIRouter, Depends, Query, Body, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.db.session import get_db
from app.db.models import BridgeCore, BridgeDetails
from app.schemas.bridge import BridgeCoreResponse, TileBatchRequest, BridgeDetailsResponse
from app.utils.bridge_service import tile_to_bbox, single_tile_query, batch_tile_query
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[BridgeCoreResponse])
def get_bridges(limit: int = Query(100), db: Session = Depends(get_db)):
    # Returns a limited number of bridge core records
    return db.query(BridgeCore).limit(limit).all()


@router.post("/batch", response_model=List[BridgeCoreResponse])
def get_bridges_by_tiles(
    req: TileBatchRequest = Body(...),
    limit: int = Query(100),
    filterKey: str = Query("default"),
    mode: str = Query("batch"),  
    db: Session = Depends(get_db)
):

    # Validate tile input
    if not req.tiles:
        raise HTTPException(status_code=400, detail="Tiles list cannot be empty.")
    
    # Validate limit
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer.")

    # Map filterKey to SQL ORDER BY clause
    match filterKey:
        case "lowestRating":
            order_clause = "lowest_rating ASC NULLS LAST"
        case "highestADT":
            order_clause = "adt_029 DESC NULLS LAST"
        case "worstBridgeCondition":
            order_clause = "bridge_condition ASC NULLS LAST"
        case _:
            raise HTTPException(
                status_code=400,
                detail="Invalid filterKey. Must be one of: lowestRating, highestADT, worstBridgeCondition."
            )

    try:
        # Run query per tile 
        if mode == "single":
            result = single_tile_query(req, limit, order_clause, db)
        # Run spatial union query across all tiles (batch mode)
        else:
            result = batch_tile_query(req, limit, order_clause, db)
        
        # Return result rows as dictionaries
        return [dict(row) for row in result]
    
    except Exception as e:
        logger.exception("Failed to fetch bridges")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        

@router.get("/detail/{structure_number}", response_model=BridgeDetailsResponse)
def get_bridge_details(structure_number: str, db: Session = Depends(get_db)):

    # Fetch detailed bridge info using structure number
    bridge = db.query(BridgeDetails).filter(
        BridgeDetails.structure_number_008 == structure_number
    ).first()

    # Return 404 if not found
    if not bridge:
        raise HTTPException(status_code=404, detail="Bridge not found")

    return bridge